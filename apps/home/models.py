# -*- coding: utf-8 -*-
from django.db import models


class Cars(models.Model):
    pk_cars = models.AutoField(primary_key=True, verbose_name='Código do Carro')
    dsc_car = models.CharField(max_length=50, verbose_name='Descrição')
    factory_serial = models.CharField(max_length=64, verbose_name='Núm. Serial')
    date_factory = models.DateTimeField(verbose_name='Data Fabr.')
    date_insert = models.DateTimeField(auto_now=True, verbose_name='Data Inserção')

    class Meta:
        db_table = 'cars'
        verbose_name_plural = 'Cars'

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
        verbose_name_plural = 'CarsBoxes'

    def clear_box_id(self, car: int = 0):
        if car == 0:
            return
        self.fisical_box_id = ''
        return

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
        verbose_name_plural = 'CarsBoxesMessages'

    def __str__(self):
        return self.box_name

