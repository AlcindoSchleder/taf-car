# -*- coding: utf-8 -*-
import os
import hashlib
import apps
import pandas as pd
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from data_control.fields import ConsincoMapping as cm
from data_control.api import ApiHostAccess
from apps.login.models import UsersOperatorsPermissions
from apps.home.models import Cars, CarsBoxes
from apps.carriers.models import (
    Products, ProductsSimilar, CargasProdutos, LastCharge,
    Carriers, CarriersProducts, CarriersBoxes
)


class Consinco2Plataform:
    FRACTIONED_PRODUCTS = ['FR', 'FL', 'CO', 'FG']

    df = None

    @staticmethod
    def get_products_from_api(api_name: str = 'all_products', **params):
        params = {} if params is None else params
        try:
            last_charge = LastCharge.objects.get()
            pk_last_charge = last_charge.pk_last_charge
        except ObjectDoesNotExist:
            pk_last_charge = 0
        params['pk_charge'] = pk_last_charge
        api = ApiHostAccess()
        return api.get_data(api_name, **params)

    @staticmethod
    def _create_hash_from_fields(**fields):
        pk = ''
        for field in fields:
            pk += str(fields[field]) + '-'
        hash_object = hashlib.sha256(pk[0:-1].encode())
        return hash_object.hexdigest()

    @staticmethod
    def _convert_product(row):
        data = {}
        for f in cm.PRODUCTS_MAP:
            if f in row.keys():
                data[cm.PRODUCTS_MAP[f]] = row[f]
        return data

    @staticmethod
    def _save_df(row: dict, table):
        data = row
        if type(row) is list:
            for reg in row:
                data = table(**reg)
                data.save()
        else:
            if row.get('status') and row['status'].get('sttCode') != 200:
                return row
            data = table(**row)
            data.save()
        return data

    def _save_charge_products(self) -> bool:
        self.df = self.df[self.df['tipseparacao'].isin(self.FRACTIONED_PRODUCTS)]
        res = apps.result_dict()
        try:
            data = None
            for index, row in self.df.iterrows():
                data = CargasProdutos(**row)
                data.save()
            reg = LastCharge(
                fk_cargas_produtos=data,
                pk_last_charge=data.nrocarga,
                date_last_charge=datetime.now(tz=timezone.utc)
            )
            reg.save()
        except Exception as e:
            res['status']['sttCode'] = 500
            res['status']['sttMsgs'] = f'Erro: ao salvar o Data Frame - {e}'
            return res
        return res

    def _test_data_frame_fields(self, flag_from_data: bool):
        index = self.df.shape
        if (flag_from_data == 2) or (flag_from_data == 3):
            if index[1] >= len(cm.API_FIELDS):
                for field in cm.API_FIELDS:
                    flag = field in self.df.columns
                    if not flag:
                        return False
            else:
                return False
        else:
            return False
        self.df = self.df[cm.API_FIELDS]

        row = self.df.iloc[index[0] - 1]
        pk_charge = row['nrocarga']
        try:
            res = CargasProdutos.objects.filter(nrocarga=pk_charge).count() == 0
        except ObjectDoesNotExist:
            res = True
        return res

    def _convert_products_similar(self, row):
        param = row.copy()
        api = ApiHostAccess()
        res = api.get_data('product_pk', pk_product=param['seqproduto'])
        data = res['data'].get('records') if res.get('data') is not None else None
        if data is None:
            return res
        records = []
        if len(data) > 0:
            for record in data:         # le os registros retornados da api
                for idx in record:      # le os campos do registro
                    param[idx] = record[idx]
                records.append(param)

        data = {}
        res = []
        for param in records:
            for f in cm.PRODUCTS_SIMILAR_MAP:
                data['fk_products_id'] = param['seqproduto']
                if f in param.keys():
                    data[cm.PRODUCTS_SIMILAR_MAP[f]] = param[f]
            res.append(data)
        return res

    def _convert_carrier(self, row):
        param = row.copy()
        # pk_carriers, lot, fk_customers
        pk = self._create_hash_from_fields(
            pk_carriers=row["nrocarga"],
            lot=row["seqlote"],
            fk_customer=row["seqpessoa"]
        )
        data = {
            'pk_carriers': pk,

        }
        fields = cm.CARRIERS_MAP.copy()
        del fields['pk_carriers']
        for f in fields:
            if f in param.keys():
                data[fields[f]] = param[f]
            else:
                data[f] = fields[f]
        return data

    def _check_product(self, row):
        try:
            date = datetime.now().replace(
                hour=00, minute=00, second=00, microsecond=00
            )
            product = Products.objetcs.get(
                pk_products=row['seqproduto'],
                update_date__lt=date
            )
        except ObjectDoesNotExist:
            product = None
        if product is None:
            product = self._save_df(self._convert_product(row), Products)
            if type(product) is dict:
                return product
            product_similar = self._save_df(self._convert_products_similar(row), ProductsSimilar)
            if type(product_similar) is dict:
                return product_similar
        return product

    def _convert_carrier_products(self, row, fk_carrier: str):
        param = row.copy()

        # check if products already registered and if it is updated
        res = self._check_product(row)
        if type(res) is dict:
            return res

        # pk_carriers, fk_products, street e tower
        pk = self._create_hash_from_fields(
            pk_carriers_id=row["nrocarga"],
            fk_products_id=row["seqproduto"],
            street=row["codrua"],
            tower=row['nropredio']
        )
        data = {
            'pk_carriers_products': pk,
            'fk_carriers_id': fk_carrier,
            'fk_products_id': row['seqproduto'],
        }
        fields = cm.CARRIERS_PRODUCTS_MAP.copy()
        del fields['pk_carriers_products']
        del fields['fk_carriers']
        del fields['seqproduto']
        del fields['fk_products_similar']
        for f in fields:
            if f in param.keys() and type(f) == 'str':
                data[fields[f]] = param[f]
            else:
                data[f] = fields[f]
        return data

    def _convert_carrier_boxes(self, row, pk_carriers_products):
        param = row.copy()
        # pk_carriers_products, fk_users e fk_cars_boxes
        pk = self._create_hash_from_fields(
            pk_carriers=row["nrocarga"],
            fk_products=row["seqlote"],
            street=row["seqpessoa"],
            tower=row['nropredio']
        )
        data = {
            'pk_carriers_products': pk,
            'fk_users': str(apps.USER_NAME),
            'fk_cars_boxes': str(apps.CAR_ID) + '___',
        }
        fields = cm.CARRIERS_BOXES_MAP.copy()
        del fields['pk_carriers_products']
        del fields['fk_carriers']
        del fields['seqproduto']
        del fields['fk_products_similar']
        for f in fields:
            if f in param.keys() and type(f) == 'str':
                data[fields[f]] = param[f]
            else:
                data[f] = fields[f]
        return data

    def _convert_consinco_to_plataform(self):
        res = apps.result_dict()
        pk_charge = 0
        try:
            data_df = []
            for index, row in self.df.iterrows():
                # insert a charge
                if pk_charge != row['nrocarga']:
                    res = self._save_df(self._convert_carrier(row), Carriers)
                    if type(res) is dict:
                        return res
                pk_charge = res.charge
                fk_charge = res.pk_carriers

                charges = res.__dict__()

                # insert a product of the charge
                carrier_product = self._save_df(
                    self._convert_carrier_products(row, fk_charge),
                    CarriersProducts,
                )
                if type(carrier_product) is dict:
                    return carrier_product
                charges_products = cm.queryset_to_dict(carrier_product)
                all_charges = {}
                all_charges.update(charges)
                all_charges.update(charges_products)
                data_df.append(all_charges)
                # create a dataframe with new data
            self.df = pd.DataFrame(data_df)
        except Exception as e:
            res['status']['sttCode'] = 500
            res['status']['sttMsgs'] = f'Erro ao gravar os cargas da plataforma! - ({e})'
        if res['status']['sttCode'] != 200:
            return res
        return res

    def get_products_data_frame(self):
        res = apps.result_dict()
        res = self.get_products_from_api('all_products')
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
            return res, None
        self.df['status'] = 'L'
        self.df['volume'] = (self.df['altura'] / 100) * (self.df['largura'] / 100) * (self.df['profundidade'] / 100)
        """
        res['status']['from_data']:
        1: banco de dados classificado
        2: api não classificada
        3: csv semi-classificada
        """

        if self._test_data_frame_fields(res['status']['from_data']):
            res = self._save_charge_products()
        if res['status']['sttCode'] != 200:
            return res, None
        if 'data' in res.keys():
            res['data'] = []
        self.df = self.df[cm.FILTER_PROD]
        res = self._convert_consinco_to_plataform()
        return res, self.df


class ProductDataControl:
    CAR_BOXES = []
    USER_PERMISSIONS = []
    _PROTO = 'http'
    _PORT = 5180
    _TIMEOUT = 3.5
    url = None
    df = None
    df_original = None
    host = None
    pk_last_charge = 0
    date_last_charge = 0

    @staticmethod
    def create_data_frame():
        charges_list = []
        carriers = Carriers.objects.filter(flag_status='L')
        for carrier in carriers:
            carriers_products = CarriersProducts.objects.filter(fk_carriers=carrier.pk_carriers)

            charges_dict = cm.queryset_to_dict(carrier)   # create a dict from carrier
            for carrier_product in carriers_products:
                charges_dict.update(cm.queryset_to_dict(carrier_product))
                charges_list.append(charges_dict)

        return pd.DataFrame(charges_list)

    @staticmethod
    def _load_boxes():
        first_pk = int(str(apps.CAR_ID) + str(10))
        last_pk = int(str(apps.CAR_ID) + str(26))
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
                'car_id': apps.CAR_ID,
                'user_id': apps.USER_NAME,
            })
        return box_data

    def _calculate_fields(self):
        res = apps.result_dict()
        try:
            self.df['sytatus'] = 'L'
            self.df['weight_prod'] = round(self.df['qtd_packing'] * self.df['weight'], 6)
            self.df['volume_prod'] = round(self.df['qtd_packing'] * self.df['volume'], 6)
            self.df['side'] = self.df.apply(lambda row: 'E' if (row['nropredio'] % 2) == 0 else 'D', axis=1)
            # self.df['status'] = 'P'
            self.df = self.df.sort_values(cm.SEPARATION_SORT)
        except Exception as e:
            res['status']['sttCode'] = 500
            res['status']['sttMsgs'] = f'Erro ao calcular o peso e o volume dos ítens! - ({e})'
        return res

    def _filter_user_product(self):
        self.df = self.create_data_frame()      # Create a DataFram from plataform database
        res = apps.result_dict()

        # Get all users permissions
        permissions = UsersOperatorsPermissions.objects.filter(
            pk__startswith=apps.USER_NAME
        )
        for perm in permissions:
            if perm.flag_status == 'A':
                self.USER_PERMISSIONS.append(perm.type_line)
        if len(self.USER_PERMISSIONS) == 0:
            res['status']['sttCode'] = 404
            res['status']['sttMsgs'] = 'Usuário não possui ativaidades'
            return res

        # Filter users permissions from data
        self.df = self.df[self.df['flag_type_line'].isin(self.USER_PERMISSIONS)]
        sp = self.df.shape
        if sp[0] < 1:
            res['status']['sttCode'] = 404
            res['status']['sttMsgs'] = 'Usuário não possui atividades nas cargas selecionadas'
            return res

        # Calc all Fields to store into database and mount orders into car boxes
        res = self._calculate_fields()
        if res['status']['sttCode'] != 200:
            return res

        if not self._load_boxes():      # Load Boxes from CAR_ID to mount orders into car boxes
            res['status']['sttCode'] = 500
            res['status']['sttMsgs'] = 'Não foi possível carregar os pedidos nas caçambas!'
        return res

    def _get_product_data(self, pk: int = 0, barcode: str = ''):
        res = apps.result_dict()
        if pk == 0 and barcode == '':
            res['status']['sttCode'] = 403
            res['status']['sttMsgs'] = \
                'Erro: para buscar um produto, envie o código do ' \
                'produto ou o código de barras do produto'
            return res
        product = Products()
        similar = ProductsSimilar()

        # get product data from E.R.P.
        api = ApiHostAccess()
        res = api.get_data('product', seqprodudo=pk)

        if res and res['records']:
            item = res['records']

            # Save Product Data
            with cm.PRODUCTS_MAP as PM:
                for field in PM:
                    if getattr(product, PM[field]):
                        setattr(product, PM[field], item[field])
            product.save()

            # Save Product Similar Data
            with cm.PRODUCTS_SIMILAR_MAP as PSM:
                for field in PSM:
                    if getattr(similar, PSM[field]):
                        setattr(similar, PSM[field], item[field])
            similar.save()

        # set product and similar to dictionary then return it
        item = cm.queryset_to_dict(product)
        item.update(cm.queryset_to_dict(similar))
        res['data'] = item
        return res

    def _save_product_original(self, line, charge, order, product, status):
        prod = self.df_original[
            (self.df_original['tipseparacao'] == line) &
            (self.df_original['nrocarga'] == charge) &
            (self.df_original['seqpessoa'] == order) &
            (self.df_original['seqproduto'] == product)
        ]
        prod.at[prod.index[0], 'status'] = status
        pk_charge = prod.index[0]
        charge_prod = Carriers.objects.get(pk=pk_charge)
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

        sum_weight = 0.0  # acumulador de peso (juntar caixas)
        sum_volume = 0.0  # acumulador de volume (juntar caixas)

        self.df['change_msg'] = ''
        self.df['peso_box'] = 0.0  # nova coluna do peso total da caixa
        self.df['volume_box'] = 0.0  # nova coluna do volume total da caixa
        self.df['box_name'] = ''  # nova coluna do slot onde a caixa se encontra no carro
        self.df['box_id'] = ''  # nova coluna do código da caixa
        self.df = self.df.groupby(cm.COLLECT_SORT).first().copy()

        # varáveis de controle
        row_idx = 0
        box_idx = -1
        prev_line = ''
        prev_charge = 0
        for index, row in self.df[(self.df['box_id'] == '') & (self.df['status'].isin('P', 'L'))].iterrows():
            if box_idx >= apps.MAX_BOXES:  # limite de boxes do carro
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
                sum_weight += apps.BOX_MAX_WEIGHT
                sum_volume += apps.BOX_MAX_VOLUME

            # apply rules
            if sum_weight < apps.BOX_MAX_WEIGHT or sum_volume < apps.BOX_MAX_VOLUME:
                self.set_dataframe_info(box_idx, line, charge, order, product, sum_weight, sum_volume)
            else:
                box_idx += 1
                if box_idx < apps.MAX_BOXES:
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

    def _get_data_and_store_db(self):
        c2p = Consinco2Plataform()
        res, self.df = c2p.get_products_data_frame()
        return res

    @property
    def fractional_products(self):
        res = self._get_data_and_store_db()
        # if res['status']['sttCode'] == 200:
        #     res, flag_filter = self._filter_user_product()
        #     if res['status']['sttCode'] != 200:
        #         return res
        #     self._set_boxes_charge()
        #     if flag_filter == 0:
        #         res['status']['sttCode'] = 500
        #         if flag_filter == -1:
        #             res['status']['sttMsgs'] = f'Usuário {apps.USER_NAME} não ainda não possui atividades!'
        #         elif flag_filter == -2:
        #             res['status']['sttMsgs'] = f'Erro: Nenhuma caçamba foi alocada para o carro: {apps.CAR_ID}'
        #         else:
        #             res['status']['sttMsgs'] = 'Erro Desconhecido: Entre em contato com o suporte' + \
        #                                                f' e informe o seguinte código: {apps.CAR_ID}-{flag_filter}'
        return res

    @property
    def product_data(self):
        data = Carriers.objects.filter(
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
