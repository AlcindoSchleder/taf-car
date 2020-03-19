# -*- coding: utf-8 -*-
import os
import hashlib
import apps
import pandas as pd

from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from data_control.fields import ConsincoMapping as Cmp
from data_control.api import ApiHostAccess
from apps.carworker.messages import AsyncMessages
from apps.login.models import UsersOperatorsPermissions
from apps.home.models import CarsBoxes
from apps.carriers.models import (
    Products, ProductsSimilar, CargasProdutos, LastCharge,
    Carriers, CarriersProducts, CarriersBoxes
)


class Consinco2Plataform:
    FRACTIONED_PRODUCTS = ['LF', 'CO', 'FG']

    df = None
    carrier_list = []
    product_list = []
    product_similar_list = []
    carrier_product_list = []

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
    def create_hash_from_fields(**fields):
        pk = ''
        for field in fields:
            pk += str(fields[field]) + '-'
        hash_object = hashlib.sha256(pk[0:-1].encode())
        return hash_object.hexdigest()

    @staticmethod
    def _convert_product(row):
        data = {}
        for f in Cmp.PRODUCTS_MAP:
            if f in row.keys():
                data[Cmp.PRODUCTS_MAP[f]] = row[f]
        try:
            pk = data['pk_products']
            Products.objects.get(pk_products=pk)
            data['update_date'] = timezone.now()
        except ObjectDoesNotExist:
            data['insert_date'] = timezone.now()
        return Products(**data)

    @staticmethod
    def _convert_products_similar(row):
        data = {}
        for f in Cmp.PRODUCTS_SIMILAR_MAP:
            if f in row.keys():
                data[Cmp.PRODUCTS_SIMILAR_MAP[f]] = row[f]
        try:
            pk = data['pk_products_similar']
            ProductsSimilar.objects.get(pk_products_similar=pk)
            data['update_date'] = timezone.now()
        except ObjectDoesNotExist:
            data['insert_date'] = timezone.now()
        return ProductsSimilar(**data)

    @staticmethod
    def save_bulk_data(rec_list, table):
        if len(rec_list) > 0:
            size = Cmp.bath_size(table, len(rec_list))
            if size > 0:
                table.objects.bulk_create(rec_list, size)

    def _save_charge_products(self) -> dict:
        res = apps.result_dict()
        res['result_to'] = self.df.shape[0]
        try:
            data = None
            list_of_data = []
            last_data = None
            for index, row in self.df.iterrows():
                data = CargasProdutos(**row)
                list_of_data.append(data)
                if len(list_of_data) > 15:
                    self.save_bulk_data(list_of_data, CargasProdutos)
                    last_data = list_of_data[-1]
                    list_of_data = []
                # data.save()
            if len(list_of_data) > 0:
                self.save_bulk_data(list_of_data, CargasProdutos)
                last_data = list_of_data[-1]
            if last_data is not None:
                last_data.save()
                reg = LastCharge(
                    pk_last_charge=last_data.nrocarga,
                    fk_cargas_produtos_id=last_data.pk_cargas_produtos,
                    fk_company=last_data.nroempresa,
                    num_lot=last_data.seqlote,
                    fk_product=last_data.seqproduto,
                    fk_customer=last_data.seqpessoa,
                    date_last_charge=timezone.now()
                )
                reg.save()
        except Exception as e:
            res['status']['sttCode'] = 500
            res['status']['sttMsgs'] = f'Erro: ao salvar o Data Frame - {e}'
        return res

    def _test_data_frame_fields(self, flag_from_data: bool):
        index = self.df.shape
        if (flag_from_data == 2) or (flag_from_data == 3):
            if index[1] >= len(Cmp.API_FIELDS):
                for field in Cmp.API_FIELDS:
                    flag = field in self.df.columns
                    if not flag:
                        return False
            else:
                return False
        else:
            return False
        self.df = self.df[Cmp.API_FIELDS]

        row = self.df.iloc[index[0] - 1]
        pk_charge = row['nrocarga']
        try:
            res = CargasProdutos.objects.filter(nrocarga=pk_charge).count() == 0
        except ObjectDoesNotExist:
            res = True
        return res

    def _convert_carrier(self, row):
        param = row.copy()
        # pk_carriers, lot, fk_customers
        pk = self.create_hash_from_fields(
            pk_carriers=row["nrocarga"],
            lot=row["seqlote"],
            fk_customer=row["seqpessoa"]
        )
        data = {
            'pk_carriers': pk,

        }
        fields = Cmp.CARRIERS_MAP.copy()
        del fields['pk_carriers']
        for f in fields:
            if f in param.keys():
                data[fields[f]] = param[f]
            else:
                data[f] = fields[f]
        try:
            Carriers.objects.get(pk_carriers=pk)
            data['update_date'] = timezone.now()
        except ObjectDoesNotExist:
            data['insert_date'] = timezone.now()
        return Carriers(**data)

    def _convert_carrier_products(self, row, fk_carrier: str):
        param = row.copy()

        # charge, fk_customers, fk_products, street and tower
        pk = self.create_hash_from_fields(
            fk_carriers=row["nrocarga"],
            fk_customer=row["seqpessoa"],
            fk_products=row["seqproduto"],
            street=row["codrua"],
            tower=row['nropredio'],
        )
        data = {
            'pk_carriers_products': pk,
            'fk_carriers_id': fk_carrier,
        }
        fields = Cmp.CARRIERS_PRODUCTS_MAP.copy()
        del fields['pk_carriers_products']
        del fields['fk_carriers_id']
        for f in fields:
            if f in param.keys():
                data[fields[f]] = param[f]
        return CarriersProducts(**data)

    def _get_product_similar_to_list(self, df_row):
        param = df_row.copy()
        api = ApiHostAccess()
        res = api.get_data('product_pk', pk_product=df_row['seqproduto'])
        records = res['data'].get('records') if res.get('data') is not [] else None
        for record in records:         # le os registros retornados da api
            param['imagem'] = record['imagem'][2:-1]
            param['codacesso'] = record['codacesso']
            data = self._convert_products_similar(param)
            if data.update_date:
                data.save()
            else:
                if data not in self.product_similar_list:
                    self.product_similar_list.append(data)
            if len(self.product_similar_list) > 25:
                if len(self.product_list) > 0:
                    self.save_bulk_data(self.product_list, Products)
                    self.product_list = []
                self.save_bulk_data(self.product_similar_list, ProductsSimilar)
                self.product_similar_list = []

    def _get_product_to_list(self, df_row):
        data = self._convert_product(df_row)
        if data.update_date:
            data.save()
        else:
            if data not in self.product_list:
                self.product_list.append(data)

    def _get_carrier_to_list(self, df_row):
        data = self._convert_carrier(df_row)
        if data.update_date:
            data.save()
        else:
            self.carrier_list.append(data)
        if len(self.carrier_list) > 35:
            self.save_bulk_data(self.carrier_list, Carriers)
            self.carrier_list = []
        return data.charge, data.pk_carriers

    def _get_carrier_product_to_list(self, df_row, fk_carrier: str):
        data = self._convert_carrier_products(df_row, fk_carrier)
        if data.update_date:
            data.save()
        else:
            self.carrier_product_list.append(data)
        if len(self.carrier_product_list) > 25:
            if len(self.product_list) > 0:
                self.save_bulk_data(self.product_list, Products)
                self.product_list = []
            if len(self.carrier_list) > 0:
                self.save_bulk_data(self.carrier_list, Carriers)
                self.carrier_list = []
            self.save_bulk_data(self.carrier_product_list, CarriersProducts)
            self.carrier_product_list = []

    def _convert_consinco_to_plataform(self):

        res = apps.result_dict()
        pk_charge = 0
        try:
            self.carrier_list = []
            self.product_list = []
            self.product_similar_list = []
            self.carrier_product_list = []
            data = None
            fk_carriers = ''

            for index, row in self.df.iterrows():
                # insert a charge
                if pk_charge != row['nrocarga']:
                    pk_charge, fk_carriers = self._get_carrier_to_list(row)

                # check if products already registered and if it is updated
                self._get_product_to_list(row)
                self._get_product_similar_to_list(row)
                self._get_carrier_product_to_list(row, fk_carriers)

            self.save_bulk_data(self.carrier_list, Carriers)
            self.save_bulk_data(self.product_list, Products)
            self.save_bulk_data(self.product_similar_list, ProductsSimilar)
            self.save_bulk_data(self.carrier_product_list, CarriersProducts)
            self.df = None
        except Exception as e:
            res = apps.result_dict()
            res['status']['sttCode'] = 500
            res['status']['sttMsgs'] = f'Erro ao gravar os cargas da plataforma! - ({e})'
        if res['status']['sttCode'] != 200:
            return res
        return res

    def get_products_data_frame(self):

        def calc_volume(x):
            return (x['altura'] / 100) * (x['largura'] / 100) * (x['profundidade'] / 100)

        def get_side(x):
            return 'E' if (x['nropredio'] % 2) == 0 else 'D'

        # res = apps.result_dict()
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
        self.df['volume'] = self.df.apply(calc_volume, axis=1)
        self.df['side'] = self.df.apply(get_side, axis=1)
        """
        res['status']['from_data']:
        1: banco de dados classificado
        2: api não classificada
        3: csv semi-classificada
        """

        self.df = self.df[self.df['tipseparacao'].isin(self.FRACTIONED_PRODUCTS)]
        if self._test_data_frame_fields(res['status']['from_data']):
            res = self._save_charge_products()
        if res['status']['sttCode'] != 200:
            return res, None     # DataFrame must be None
        if res.get('data') is not None:
            res['data'] = []
        self.df = self.df[Cmp.FILTER_PROD]
        res = self._convert_consinco_to_plataform()
        return res, self.df


class ProductDataControl:
    CAR_BOXES = []
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
    def get_allocation_boxes():
        pk_cars_gt = int(f'{apps.CAR_ID}10')
        pk_cars_lt = int(f'{apps.CAR_ID}{apps.CAR_LEVELS}{apps.CAR_BOXES_LEVEL}')
        boxes = CarsBoxes.objects.filter(pk__range=(pk_cars_gt, pk_cars_lt), fisical_box_id__isnull=False)
        apps.CAR_PREPARED = boxes.count() == (apps.CAR_LEVELS * apps.CAR_BOXES_LEVEL)
        if apps.CAR_PREPARED:
            for box in boxes:
                display_id = box.box_name
                box_id = box.fisical_box_id
                AsyncMessages.send_message_to_member('control', apps.CAR_ID, display_id, box_id)
        return apps.CAR_PREPARED

    @staticmethod
    def load_boxes():
        first_pk = int(str(apps.CAR_ID) + str(10))
        last_pk = int(str(apps.CAR_ID) + str(26))
        boxes = CarsBoxes.objects.filter(pk__gt=first_pk, pk__lt=last_pk)
        if boxes.count() <= 0:
            return False
        box_data = []
        for box in boxes:
            box_data.append({
                'name': box.box_name,
                'box_id': box.fisical_box_id,
                'weight': box.weight,
                'volume': box.volume,
                'key': box.charge_key,
                'car_id': apps.CAR_ID,
                'user_id': apps.USER_NAME,
            })
        return box_data

    @staticmethod
    def _get_data_and_store_db():
        c2p = Consinco2Plataform()
        res = c2p.get_products_data_frame()
        return res

    def set_data_frame_info(self, idx, line, charge, order, product, weight_box, volume_box):
        self.CAR_BOXES[idx]['key'] = f'{line}|{charge}|{order}'
        self.CAR_BOXES[idx]['weight'] = weight_box
        self.CAR_BOXES[idx]['volume'] = volume_box
        # save box data
        self.df.loc[line].loc[charge].loc[order].at[product, 'box_name'] = self.CAR_BOXES[idx]['name']
        self.df.loc[line].loc[charge].loc[order].at[product, 'box_id'] = self.CAR_BOXES[idx]['box_id']
        self.df.loc[line].loc[charge].loc[order].at[product, 'weight_box'] = weight_box
        self.df.loc[line].loc[charge].loc[order].at[product, 'volume_box'] = volume_box
        self.df.loc[line].loc[charge].loc[order].at[product, 'status'] = 'S'

        # save charge car data
        fk_carriers_products =  self.df.loc[line].loc[charge].loc[order].at[product, 'pk_carriers_products']
        fk_cars_boxes = str(apps.CAR_ID) + self.CAR_BOXES[idx]['name']
        pk = Consinco2Plataform.create_hash_from_fields(
            fk_carriers_products=fk_carriers_products,
            fk_users=str(apps.USER_NAME),
            fk_cars_boxes=fk_cars_boxes
        )

        carrier_box_data = {
            'pk_carrier_boxes': pk,
            'fk_carriers_products_id': fk_carriers_products,
            'fk_cars_id': apps.CAR_ID,
            'fk_cars_boxes_id': fk_cars_boxes,
            'fk_users_id': str(apps.USER_NAME),
            'weight_box': weight_box,
            'volume_box': volume_box,
            'insert_date': timezone.now()
        }
        carrier_box = CarriersBoxes(**carrier_box_data)
        carrier_box.save()
        # self._save_product_original(line, charge, order, product, 'S')

    def _set_boxes_charge(self):
        # TODO:  buscar de parâmetros no database

        sum_weight = 0.0  # acumulador de peso (juntar caixas)
        sum_volume = 0.0  # acumulador de volume (juntar caixas)

        self.df['change_msg'] = ''
        self.df['weight_box'] = 0.0  # nova coluna do peso total da caixa
        self.df['volume_box'] = 0.0  # nova coluna do volume total da caixa
        self.df['box_name'] = ''  # nova coluna do slot onde a caixa se encontra no carro
        self.df['box_id'] = ''  # nova coluna do código da caixa
        self.df = self.df.groupby(Cmp.COLLECT_SORT).first().copy()

        # varáveis de controle
        row_idx = 0
        box_idx = -1
        prev_line = ''
        prev_charge = 0
        for index, row in self.df[(self.df['box_id'] == '') & (self.df['flag_status'].isin(('P', 'L')))].iterrows():
            if box_idx >= apps.MAX_BOXES:  # limite de boxes do carro
                break
            line = self.df.index[row_idx][0]
            charge = self.df.index[row_idx][1]
            order = self.df.index[row_idx][2]
            product = self.df.index[row_idx][3]
            weight_prod = self.df.loc[line].loc[charge].loc[order].at[product, 'weight_prod']
            volume_prod = self.df.loc[line].loc[charge].loc[order].at[product, 'volume_prod']

            self.df.loc[line].loc[charge].loc[order].at[product, 'flag_status'] = 'P'
            # self._save_product_original(line, charge, order, product, 'S')

            sum_weight += weight_prod
            sum_volume += volume_prod

            # print first register (linha_ant == '')
            if prev_line != line or prev_charge != charge:  # mudou a linha ou a carga ou o lote muda a caixa
                change_label = ''
                if prev_charge != line:
                    change_label = 'carga'
                if prev_line != line:
                    change_label = 'linha'
                msg = f'mudou a {change_label}: ', line, charge, order, box_idx
                self.df.loc[line].loc[charge].loc[order].at[product, 'change_msg'] = msg
                sum_weight += apps.BOX_MAX_WEIGHT
                sum_volume += apps.BOX_MAX_VOLUME

            # apply rules
            if sum_weight < apps.BOX_MAX_WEIGHT or sum_volume < apps.BOX_MAX_VOLUME:
                self.set_data_frame_info(box_idx, line, charge, order, product, sum_weight, sum_volume)
            else:
                box_idx += 1
                if box_idx < apps.MAX_BOXES:
                    self.set_data_frame_info(box_idx, line, charge, order, product, sum_weight, sum_volume)
                sum_weight = weight_prod
                sum_volume = volume_prod
            prev_line = line
            prev_charge = charge
            row_idx += 1

    def _filter_user_product(self):
        res = apps.result_dict()

        # Get all users permissions
        permissions = UsersOperatorsPermissions.objects.filter(
            pk__startswith=apps.USER_NAME
        )
        for perm in permissions:
            if perm.flag_status == 'A':
                apps.USER_PERMISSIONS.append(perm.type_line)
        if len(apps.USER_PERMISSIONS) == 0:
            res['status']['sttCode'] = 404
            res['status']['sttMsgs'] = 'Usuário não possui atividades!'
            return res

        # Filter users permissions from data
        self.df = self.df[self.df['flag_type_line'].isin(apps.USER_PERMISSIONS)]
        sp = self.df.shape
        if sp[0] < 1:
            res['status']['sttCode'] = 404
            res['status']['sttMsgs'] = 'Usuário não possui atividades nas cargas selecionadas'
            return res
        return res

    def load_boxes_from_operator(self):

        def dictfetchall(qry_cursor):
            """
            Return all rows from a cursor as a dict
            """
            columns = [col[0] for col in qry_cursor.description]
            return [
                dict(zip(columns, qry_row))
                for qry_row in qry_cursor.fetchall()
            ]

        products_query = """
select icr.flag_type_line, icr.charge, icr.lot, icr.fk_customer, 
       ipr.pk_products, ipr.dsc_prod, icp.street, icp.tower, icp.side, 
	   icp.qtd_packing , icp.qtd_order, icp.qtd_collected, icp.unity, 
	   icp.stock, icp.weight_prod, icp.volume_prod, icr.flag_status, 
       icp.level, icp.position, icr.volume_charge, icr.weight_charge,
       icr.flag_ready, icr.flag_conference
  from icity_carriers icr, icity_carriers_products icp, icity_products ipr
 where icr.flag_status = 'L'
   and icr.flag_ready = 0
   and icr.flag_conference = 0
   and icp.fk_carriers_id = icr.pk_carriers
   and ipr.pk_products = icp.fk_products_id
 order by icr.flag_type_line, icr.charge, icr.lot, icr.fk_customer, ipr.pk_products
         """
        res = apps.result_dict()
        try:
            cursor = connection.cursor()
            cursor.execute(products_query)
            result = dictfetchall(cursor)

            self.df = pd.DataFrame(result)
        except Exception as e:
            res['status']['sttCode'] = 500
            res['status']['sttMsgs'] = f'Erro ao ler o banco de dados: {e}'
        finally:
            cursor.close()

        if res['status']['sttCode'] != 200:
            return res, None
        # res = self._filter_user_product()
        self.CAR_BOXES = self._load_boxes()
        if len(self.CAR_BOXES) > 0:
            self._set_boxes_charge()
        self.df = self.df[self.df['box_id'] != '']
        self.df.reset_index(inplace=True)
        self.df = self.df.groupby(Cmp.SEPARATION_SORT).first().copy()
        return res, self.df

    def load_all_charges(self):
        res = self._get_data_and_store_db()
        return res
