# -*- coding: utf-8 -*-
import os
import requests
import json
import datetime
import hashlib
import pandas as pd
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from taf_car.settings import API_URLS
from apps import CAR_ID, RESULT_DICT, USER_NAME, result_dict
from contrib.check import CheckHost
from apps.carriers.models import CarriersProducts, LastCharge, CarriersCars
from apps.login.models import UsersOperatorsPermissions
from apps.home.models import Cars, CarsBoxes


class ProductDataControl:

    API_FIELDS = [
        'seqproduto', 'desccompleta', 'descreduzida', 'codrua',
        'nropredio', 'nroapartamento', 'nrosala', 'especieendereco',
        'indterreoaereo', 'qtdatual', 'statusendereco', 'tipespecie',
        'nroempresa', 'nrocarga', 'coddepossepar', 'destino', 'tipentrega',
        'pesototal', 'mcubtotal', 'especieendereco.1', 'nrobox', 'statuscarga',
        'valorcarga', 'seqlote', 'qtdcontada', 'seqtarefa', 'seqatividade',
        'codtipatividade', 'nroquebra', 'mesano', 'peso', 'metragemcubica',
        'qtdvolume', 'qtditem', 'indexclusao', 'grauprioridade', 'statusrf',
        'statusatividade', 'tipseparacao', 'tiplote', 'pesototallote',
        'mcubtotallote', 'qtdvolumelote', 'qtditemlote',
        'seqordenacaoseparacao', 'seqpessoa', 'qtdembcarga', 'qtdembsolcarga',
        'qtdembsepcarga', 'nropedvenda', 'embalagem', 'pesobruto',
        'pesoliquido', 'altura', 'largura', 'profundidade'
    ]
    END_POINTS = {
        'all_products': '/tafApi/product/1.0/{p1}',
        'fractional_products': '/tafApi/product/1.0/fractional/{p1}',
        'greatness_products': '/tafApi/product/1.0/greatness/{p1}',
        'product': '/tafApi/product/1.0/%d',
        'product-image': '/tafAPI/product/1.0/pk/%s'
    }
    FILTER_PROD = [
        'seqproduto', 'desccompleta', 'qtdatual', 'qtdembcarga', 'qtdembsolcarga',
        'qtdembsepcarga', 'seqpessoa', 'embalagem', 'pesobruto', 'pesoliquido',
        'altura', 'largura', 'profundidade', 'codrua', 'nropredio', 'nroapartamento',
        'especieendereco', 'indterreoaereo', 'statusendereco', 'tipespecie',
        'nrocarga', 'tiplote', 'nrosala', 'seqlote', 'tipseparacao',
    ]

    COLLECT_SORT = [
        'tipseparacao',
        'nrocarga',
        'seqpessoa',
        'seqproduto',
    ]

    SEPARATION_SORT = [
        'street', 'tower', 'charge',
        'lot', 'pk_customer', 'level', 'position',
    ]

    CAR_BOXES = []
    USER_PERMISSIONS = []
    _PROTO = 'http'
    _PORT = 5180
    _TIMEOUT = 3.5
    result = RESULT_DICT
    url = None
    df = None
    df_original = None
    host = None
    pk_last_charge = 0
    date_last_charge = 0

    def _save_charge_products(self) -> bool:
        res = result_dict()
        try:
            data = None
            for index, row in self.df_original.iterrows():
                data = CarriersProducts(**row)
                data.save()
            reg = LastCharge(
                pk_last_charge=data.nrocarga,
                date_last_charge=datetime.now(tz=timezone.utc)
            )
            reg.save()
        except Exception as e:
            res['status']['sttCode'] = 500
            res['status']['sttMsgs'] = f'Erro: ao salvar o Data Frame - {e}'
            return res
        return res

    def _get_products_from_api(self, api_name: str = 'all_products', **params):
        res = result_dict()
        try:
            last_charge = LastCharge.objects.get()
            pk_last_charge = last_charge.pk_last_charge
        except ObjectDoesNotExist:
            pk_last_charge = 0
        check = CheckHost(API_URLS)
        self.host = check.check_hosts()
        if not self.host and api_name not in self.END_POINTS.keys():
            res['status']['sttCode'] = 404
            res['status']['sttMsgs'] = f'Error: API Host or API name {api_name} not found!'
            return res
        params = {
            'p1': pk_last_charge
        }
        end_point = self.END_POINTS[api_name].format(**params) \
            if len(params) > 0 and self.END_POINTS[api_name].find('{p') > -1 \
            else self.END_POINTS[api_name]

        self.url = f'{self._PROTO}://{self.host}:{self._PORT}{end_point}'    # mount URL
        res['url'] = self.url

        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(self.url, headers=headers)  # Call API with parameters on url
            res['status']['sttCode'] = response.status_code
            res['data'] = json.loads(response.content.decode('utf-8'))
        except Exception as e:
            res['status']['sttCode'] = 404
            res['status']['sttMsgs'] = \
                f'Error on API {api_name} ({self.url}) to load products from ERP: [{e}]'
        return res

    def _test_data_frame_fields(self, flag_from_data: bool):
        index = self.df_original.shape
        if (flag_from_data == 2) or (flag_from_data == 3):
            if index[0] == len(self.API_FIELDS):
                for field in self.API_FIELDS:
                    flag = field in self.df_original.columns
                    if not flag:
                        return False
            else:
                return False
        else:
            return False
        row = self.df_original.iloc[index[0] - 1]
        pk_charge = row['nrocarga']
        try:
            res = CarriersProducts.objects.get(nrocarga=pk_charge)
        except ObjectDoesNotExist:
            res = True
        return res

    def _get_products_data_frame(self):
        res = result_dict()
        carriers = CarriersCars.objects.filter(fk_cars_id=CAR_ID, flag_status='L')
        if carriers.count() > 0:
            pd.DataFrame(list(carriers))
            res['status']['from_data'] = 1
        else:
            res = self._get_products_from_api('all_products')
            if res['status']['sttCode'] == 200 and res['data'] is not None and len(res['data']['records']) > 0:
                self.df = pd.DataFrame(res['data']['records'])
                res['status']['from_data'] = 2
            else:
                file_name = "./temp/carga_produtos.csv"
                if os.path.exists(file_name):
                    self.df = pd.read_csv(file_name, delimiter=',', encoding='latin1')
                    res['status']['from_data'] = 3
        if self.df is None:
            res['status']['sttCode'] = 500
            res['status']['sttMsgs'] = 'Error: None data found to Data Frame!'
            return res
        self.df['status'] = 'L'
        self.df_original = self.df.copy()
        """
        res['status']['from_data']:
        1: banco de dados classificado
        2: api não classificada
        3: csv semi-classificada
        """

        if self._test_data_frame_fields(res['status']['from_data']):
            self._save_charge_products()
        res['data'] = []
        return res

    def _load_boxes(self):
        first_pk = int(str(CAR_ID) + str(10))
        last_pk = int(str(CAR_ID) + str(26))
        boxes = CarsBoxes.objects.filter(pk__gt=first_pk).AND(pk__lt=last_pk)
        if boxes.count() <= 0:
            return False
        box_data = []
        for box in boxes:
            box_data.append({
                'name': box.box_name,
                'box_id': box.fisical_box_id,
                'peso': box.weight,
                'volume': box.volume,
                'key': box.charge_key,
                'car_id': CAR_ID,
                'user_id': USER_NAME,
            })
        return box_data

    def _calculate_fields(self):
        self.df['sytatus'] = 'L'
        self.df['peso'] = round(self.df['qtdembsolcarga'] * self.df['pesobruto'], 6)
        vol_unit = self.df['altura'] * self.df['largura'] * self.df['profundidade'] / 1000000
        self.df['volume'] = round(self.df['qtdembsolcarga'] * vol_unit, 6)
        self.df['side'] = self.df.apply(lambda row: 'E' if (row['nropredio'] % 2) == 0 else 'D', axis=1)
        self.df = self.df.sort_values(self.SEPARATION_SORT)
        self.df['status'] = 'P'

    def _filter_user_product(self):
        self.df = self.df[self.FILTER_PROD]
        users = UsersOperatorsPermissions.objects.filter(pk__startswith=USER_NAME)
        for user in users:
            self.USER_PERMISSIONS.append(user.codlinhasepar)
        if self.USER_PERMISSIONS.count() == 0:  # send a message that user not has activity
            # return -1
            self.USER_PERMISSIONS = ['FR', 'FL']
        self.df = self.df[self.df['tipseparacao'].isin(self.USER_PERMISSIONS)]

        self._calculate_fields()
        if not self._load_boxes():
            return -2
        return 0

    def _get_iterrow(self, index, row):
        pk_box = int(str(CAR_ID) + str(row['box_id']))
        return {
            'fk_cars_id': CAR_ID,
            'fk_cars_boxes_id': pk_box,
            'charge': row['nrocarga'],
            'lot': row['seqlote'],
            'street': row['codrua'],
            'tower': row['nropredio'],
            'level': row['nroapartamento'],
            'position': row['nrosala'],
            'pk_product': row['seqproduto'],
            'description': row['desccompleta'],
            'stock': row['qtdatual'],
            'qtd_packing': row['qtdembcarga'],
            'qtd_order': row['qtdembsolcarga'],
            'qtd_collected': 0.0,
            'pk_customer': row['seqpessoa'],
            'unity': row['embalagem'],
            'weight': row['peso'],
            'volume': row['volume'],
            'side': row['side'],
            'flag_status': row['status'],
            'flag_ready': 0,
            'flag_conference': 0,
            'box_name': row['box_name'],
            'box_id': row['box_id'],
            'weight_box': row['weight_box'],
            'volume_box': row['volume_box']
        }

    def _save_carrier_charges(self):
        for index, row in self.df.iterrows():
            data = self._get_iterrow(index, row)
            pk = f'{USER_NAME};{CAR_ID};{data["charge"]};{data["pk_order"]};{data["box_id"]}'
            # Assumes the default UTF-8
            hash_object = hashlib.sha256(pk.encode())
            data['pk_user_products'] = hash_object.hexdigest()
            obj_data = CarriersCars(**data)
            obj_data.save()

    def _save_product_original(self, line, charge, order, product, status):
        prod = self.df_original[
            (self.df_original['tipseparacao'] == line) &
            (self.df_original['nrocarga'] == charge) &
            (self.df_original['seqpessoa'] == order) &
            (self.df_original['seqproduto'] == product)
        ]
        prod.at[prod.index[0], 'status'] = status
        pk_charge = prod.index[0]
        charge_prod = CarriersCars.objects.get(pk=pk_charge)
        charge_prod.status = status
        charge_prod.save()

    def set_dataframe_info(self, idx, line, charge, order, product, weight_box, volume_box):
        self.CAR_BOXES[idx]['key'] = f'{line}|{charge}|{order}'
        self.CAR_BOXES[idx]['peso'] = weight_box
        self.CAR_BOXES[idx]['volume'] = volume_box
        # save box data
        self.df.loc[line].loc[charge].loc[order].at[product, 'box_name'] = self.CAR_BOXES[idx]['name']
        self.df.loc[line].loc[charge].loc[order].at[product, 'box_id'] = self.CAR_BOXES[idx]['box_id']
        self.df.loc[line].loc[charge].loc[order].at[product, 'peso_box'] = weight_box
        self.df.loc[line].loc[charge].loc[order].at[product, 'volume_box'] = volume_box
        self.df.loc[line].loc[charge].loc[order].at[product, 'status'] = 'S'
        # save charge car data
        self._save_product_original(line, charge, order, product, 'S')

    def _set_boxes_charge(self):
        # TODO:  buscar de parâmetros no database
        MAX_BOXES = 10  # máximo de caixas no carro
        MAX_BOX_WEIGHT = 30  # peso máximo por caixa
        MAX_BOX_VOLUME = 0.06048  # volume máximo por caixa

        sum_weight = 0.0  # acumulador de peso (juntar caixas)
        sum_volume = 0.0  # acumulador de volume (juntar caixas)

        self.df['change_msg'] = ''
        self.df['peso_box'] = 0.0  # nova coluna do peso total da caixa
        self.df['volume_box'] = 0.0  # nova coluna do volume total da caixa
        self.df['box_name'] = ''  # nova coluna do slot onde a caixa se encontra no carro
        self.df['box_id'] = ''  # nova coluna do código da caixa
        self.df = self.df.groupby(self.COLLECT_SORT).first().copy()

        # varáveis de controle
        row_idx = 0
        box_idx = -1
        prev_line = ''
        prev_charge = 0
        for index, row in self.df[(self.df['box_id'] == '') & (self.df['status'].isin('P', 'L'))].iterrows():
            if box_idx >= MAX_BOXES:  # limite de boxes do carro
                break
            line = self.df.index[row_idx][0]
            charge = self.df.index[row_idx][1]
            order = self.df.index[row_idx][2]
            product = self.df.index[row_idx][3]
            weight_prod = self.df.loc[line].loc[charge].loc[order].at[product, 'peso_total']
            volume_prod = self.df.loc[line].loc[charge].loc[order].at[product, 'volume_itens']

            self.df.loc[line].loc[charge].loc[order].at[product, 'status'] = 'P'
            self._save_product_original(line, charge, order, product, 'S')

            sum_weight += weight_prod
            sum_volume += volume_prod
            flag_force_next_box = False

            # print first register (linha_ant == '')
            if prev_line != line or prev_charge != charge:  # mudou a linha ou a carga ou o lote muda a caixa
                change_label = ''
                if prev_charge != line:
                    change_label = 'carga'
                if prev_line != line:
                    change_label = 'linha'
                msg = f'mudou a {change_label}: ', line, charge, order, box_idx
                self.df.loc[line].loc[charge].loc[order].at[product, 'change_msg'] = msg
                flag_force_next_box = True
                sum_weight += MAX_BOX_WEIGHT
                sum_volume += MAX_BOX_VOLUME

            # apply rules
            if sum_weight < MAX_BOX_WEIGHT or sum_volume < MAX_BOX_VOLUME:
                self.set_dataframe_info(box_idx, line, charge, order, product, sum_weight, sum_volume)
            else:
                box_idx += 1
                if box_idx < MAX_BOXES:
                    self.set_dataframe_info(box_idx, line, charge, order, product, sum_weight, sum_volume)
                sum_weight = weight_prod
                sum_volume = volume_prod
            # else:
            # TODO: o peso ou o volume do pedido é maior que o peso ou o volume máximo permitido
            #       descontroi pedido e soma-se os ítens dividindo-os em boxes que alcancem a regra estabelecida
            #       resumindo aqui o pedido é divido em 2 ou mais caixas para satisfazer a regra de peso e volume máximo
            prev_line = line
            prev_charge = charge
            row_idx += 1

    @property
    def fractional_products(self):
        self.result = self._get_products_data_frame()
        if self.result['status']['sttCode'] == 200:
            self.result = result_dict()
            flag_filter = self._filter_user_product()
            if flag_filter == 0:
                self._set_boxes_charge()
                self._save_carrier_charges()
                self.result['status']['sttCode'] = 200
                self.result['status']['sttMsgs'] = 'Operação realizada com sucesso'
            else:
                self.result['status']['sttCode'] = 500
                if flag_filter == -1:
                    self.result['status']['sttMsgs'] = f'Usuário {USER_NAME} não ainda não possui atividades!'
                elif flag_filter == -2:
                    self.result['status']['sttMsgs'] = f'Erro: Nenhuma caçamba foi alocada para o carro: {CAR_ID}'
                else:
                    self.result['status']['sttMsgs'] = 'Erro Desconhecido: Entre em contato com o suporte' + \
                                                       f' e informe o seguinte código: {CAR_ID}-{flag_filter}'
        return self.result

    @property
    def product_data(self):
        data = CarriersCars.objects.filter(
            qtd_collected__gt=0, flag_status='S', flag_ready=0, flag_conference=0
        ).orderby(
            'street', 'tower', 'charge', 'lot', 'pk_customer', 'level', 'position'
        )
        if data.count > 0:
            params = {
                'address': f'{data.street}.{data.tower}.{data.position}',
                'qtd_order': data.qtd_order,
                'unity': data.unity,
                'description': data.fk_products.dsc_prod,
                'weight': data.weight,
                'volume': data.volume,
            }
            return params
        else:
            return None
