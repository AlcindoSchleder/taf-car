# -*- coding: utf-8 -*-
import apps
from django.db import models
from .choices import SEPARATION_STRINGS_OPTIONS, SORT_STRINGS_OPTIONS


class ApiHosts(models.Model):
    TYPE_NET_OPTIONS = [
        (0, 'LAN'),
        (1, 'WAN'),
    ]
    FLAG_ACTIVE_OPTIONS = [
        (0, 'Inativo'),
        (1, 'Ativo')
    ]
    pk_api_hosts = models.AutoField(primary_key=True, verbose_name='Código')
    dsc_host = models.CharField(max_length=50, verbose_name='Descrição')
    type_net = models.SmallIntegerField(choices=TYPE_NET_OPTIONS, default=0, verbose_name='Tipo NET')
    address = models.GenericIPAddressField(default='127.0.0.1', verbose_name='IP')
    port = models.IntegerField(default=5180, verbose_name='Porta')
    flag_active = models.SmallIntegerField(default=0, choices=FLAG_ACTIVE_OPTIONS, verbose_name='Ativo')
    insert_date = models.DateTimeField(auto_now=True, verbose_name='Data Inserção')

    class Meta:
        db_table = 'icity_hosts'
        verbose_name_plural = 'hosts'

    def __str__(self):
        return f'{self.dsc_host} - {self.address}:{self.port} -> {self.FLAG_ACTIVE_OPTIONS[self.flag_active][1]}'
    # TODO: Create a signal before post to check if active host is unique


class Parameters(models.Model):
    pk_parameters = models.SmallIntegerField(
        primary_key=True, editable=False, default=1, verbose_name='Parâmetro'
    )
    car_levels = models.SmallIntegerField(default=2, verbose_name='Qtd. Níveis')
    box_per_level = models.SmallIntegerField(default=5, verbose_name='Qtd. Caixas p/Nível')
    box_max_weight = models.FloatField(default=30.00, verbose_name='Peso Máximo da Caixa')
    box_max_volume = models.FloatField(default=0.054432, verbose_name='Volume Máximo da Caixa')
    volume_percent = models.FloatField(default=30.00, verbose_name='Percentual do Volume')
    fractioned_strings = models.TextField(verbose_name='Strings da Linha Fracionada')
    largest_strings = models.TextField(verbose_name='Strings da Linha Grandeza')
    load_charge_strings = models.TextField(
        choices=SEPARATION_STRINGS_OPTIONS, verbose_name='Modo de Classificação')
    Separation_charge_strings = models.TextField(
        choices=SORT_STRINGS_OPTIONS, verbose_name='Modo de Separação')
    fk_api_hosts = models.ForeignKey(
        ApiHosts, on_delete=models.CASCADE, default=1, verbose_name='Host da API default'
    )

    class Meta:
        db_table = 'icity_parameters'
        verbose_name_plural = 'Parametros'

    def __str__(self):
        return f'parâmetro: {self.pk_parameters}'


class Cars(models.Model):
    pk_cars = models.AutoField(primary_key=True, verbose_name='Código do Carro')
    dsc_car = models.CharField(max_length=50, verbose_name='Descrição')
    factory_serial = models.CharField(max_length=64, verbose_name='Núm. Serial')
    date_factory = models.DateTimeField(verbose_name='Data Fabr.')
    date_insert = models.DateTimeField(auto_now=True, verbose_name='Data Inserção')

    class Meta:
        db_table = 'cars'
        verbose_name_plural = 'Carros'

    def __str__(self):
        return self.dsc_car


class CarsBoxes(models.Model):
    # pk is composed of the car code and the code of each box = int((str(CAR_ID) + str(BOX_ID)))
    # BOX_ID is int(str(level) + str(box))
    pk_carsboxes = models.IntegerField(primary_key=True, default=0, verbose_name='Identificação')
    box_name = models.CharField(max_length=30, verbose_name='Nome do Box')
    fk_cars = models.ForeignKey(Cars, on_delete=models.CASCADE, verbose_name='Carro')
    fisical_box_id = models.CharField(
        blank=True, null=True, max_length=20, verbose_name='Código da Caçamba'
    )
    level = models.SmallIntegerField(verbose_name='Nível')
    box = models.SmallIntegerField(verbose_name='Box')
    # string that store line, charge and order separated by lines (1 box can hold multiple orders)
    charge_key = models.TextField(blank=True, null=True, verbose_name='Carga Vinculada')
    weight = models.DecimalField(
        null=True, blank=True, max_digits=9, decimal_places=4, verbose_name='Peso Máx.'
    )
    volume = models.DecimalField(
        null=True, blank=True, max_digits=9, decimal_places=4, verbose_name='Volume Máx.'
    )

    class Meta:
        db_table = 'cars_boxes'
        verbose_name_plural = 'Boxes'

    @staticmethod
    def validate_boxes(data: dict) -> dict:
        flag_validate = True
        msg_validate = ''
        for key in data:
            value = data[key][0]
            box_level = key[1]
            box_box = key[2]
            if list(data.values()).count(value) > 1 or value == '':
                flag_validate = False
                msg_validate = 'Duplicidade de caçambas detectada '
                msg_validate += f'(nível: {box_level} posição: {box_box} código: {value}).'
                break
            if str(box_level) not in apps.CAR_BOXES.keys():
                apps.CAR_BOXES[str(box_level)] = {}
            apps.CAR_BOXES[str(box_level)][str(box_box)] = value
        return {
            "car_id": apps.CAR_ID,
            "car_prepared": int(flag_validate),
            "flag_validate": int(flag_validate),
            "message": msg_validate,
        }

    @staticmethod
    def save_data(data: dict):
        if 'csrfmiddlewaretoken' in data.keys():
            del data['csrfmiddlewaretoken']
        res = CarsBoxes.validate_boxes(data)
        if not bool(res['flag_validate']):
            return False, res
        for level in apps.CAR_BOXES:
            for box in apps.CAR_BOXES[level]:
                pk = int(str(apps.CAR_ID) + str(level) + str(box))
                try:
                    car = Cars.objects.get(pk=apps.CAR_ID)
                    car_box = CarsBoxes()
                    car_box.pk_carsboxes = pk
                    car_box.box_name = f'e{level}{box}'
                    car_box.fisical_box_id = apps.CAR_BOXES[level][box]
                    car_box.level = level
                    car_box.box = box
                    car_box.weight = 0
                    car_box.volume = 0
                    car_box.fk_cars = car
                    car_box.charge_key = None   # TODO: Este campo deve conter as chaves dos cargas e pedidos dos clientes. Dicionário json em string
                    car_box.save()
                except Exception as e:
                    return False, {'msg': f'Error when save carboxes! ({e})'}
        return True, {'msg': ''}

    def __str__(self):
        return self.fk_cars.dsc_car + ' - box:' + self.box_name


class CarBoxesMessage(models.Model):
    pk_car_boxes_message = models.AutoField(primary_key=True, verbose_name='Código do Carro')
    fk_car_boxes = models.ForeignKey(CarsBoxes, on_delete=models.CASCADE, verbose_name='Box')
    flag_captured = models.SmallIntegerField(default=0, verbose_name='Capturado')
    box_type_command = models.CharField(max_length=30, verbose_name='Tipo de Comando')
    box_name = models.CharField(max_length=3, verbose_name='Nomeclatura')
    fk_cars = models.ForeignKey(Cars, on_delete=models.PROTECT, verbose_name='Carro')
    box_message = models.TextField(verbose_name='Mensagem')
    capture_date = models.DateTimeField(null=True, blank=True, verbose_name='Data de Captura')
    update_date = models.DateTimeField(null=True, blank=True, verbose_name='Data de Edicao')
    insert_date = models.DateTimeField(auto_now=True, verbose_name='Data Insercao')

    class Meta:
        db_table = 'cars_boxes_message'
        verbose_name_plural = 'Mensagens'

    def __str__(self):
        return self.box_name

