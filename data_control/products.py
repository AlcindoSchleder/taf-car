# -*- coding: utf-8 -*-
import requests
import json
import datetime
import hashlib
import pandas as pd
from taf_car.settings import API_URLS
from apps import RESULT_DICT, USER_NAME
from contrib.check import CheckHost
from apps.carriers.models import CarriersProducts, LastProductCharge, UserProducts


class ProductDataControl:

    END_POINTS = {
        'all_products': '/tafApi/product/1.0/',
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
        'nrocarga', 'tiplote', 'nrosala',
    ]

    GROUP_BY_FIELDS = [
        'nrocarga',
        'tiplote',
        'codrua',
        'nropredio',
        'nroapartamento',
        'nrosala',
        'seqpessoa'
    ]

    _PROTO = 'http'
    _PORT = 5180
    _TIMEOUT = 3.5
    result = RESULT_DICT
    url = f'{_PROTO}://%s:{_PORT}%s'
    df = None
    host = None

    def _save_charge_products(self) -> bool:
        try:
            date = datetime.datetime.now()
            reg = LastProductCharge(pk_last_product_charge=1, last_charge=date)
            reg.save()
            for index, row in self.df.iterrows():
                data = CarriersProducts(**row)
                data.save()
        except Exception as e:
            return e == ''
        return True

    def _get_products_from_api(self, api_name: str = 'all_products', **params):
        self.result = RESULT_DICT
        check = CheckHost(API_URLS)
        self.host = check.check_hosts()
        if not self.host and api_name not in self.END_POINTS.keys():
            self.result['status']['sttCode'] = 404
            self.result['status']['sttMsgs'] = f'Error: API Host or API name {api_name} not found!'
            return self.result

        # TODO: 1) Separate routes on all, fractional, and greatness products
        #       2) Load API parameter on API ENDPOINT
        end_point = self.END_POINTS[api_name].format(**params) \
            if len(params) > 0 and self.END_POINTS[api_name].find('{p') > -1 \
            else self.END_POINTS[api_name]

        self.url = self.url % self.host, end_point    # mount URL
        self.result['url'] = self.url

        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(self.url, headers=headers)  # Call API with parameters on url
            self.result['status']['sttCode'] = response.status_code
            self.result['data'] = json.loads(response.content.decode('utf-8'))
        except Exception as e:
            self.result['status']['sttCode'] = 500
            self.result['status']['sttMsgs'] = f'Error on API {api_name} to load products from ERP: [{e}]'
        return self.result

    def _get_products_data_frame(self):
        self._get_products_from_api('all_products')
        if self.result['status']['sttCode'] == 200 and self.result['data'] is not None:
            self.df = pd.DataFrame(self.result['data']['records'])
            self._save_charge_products()
        self.result['data'] = []

    def _filter_user_product(self):
        # df = self.df[self.df['tipseparacao'].isin(USER_PERMISSIONS)].copy()
        prod = self.df[self.FILTER_PROD].copy()
        prod['peso'] = prod['qtdembsolcarga'] * prod['pesobruto']
        prod['volume_m3'] = prod['qtdembcarga'] * (prod['altura'] * prod['largura'] * prod['profundidade']) / 1000000
        return prod.groupby(by=self.GROUP_BY_FIELDS)

    def _get_iterrow(self, index, row):
        return {
                'charge': index[0],
                'lot': index[1],
                'street': index[2],
                'tower': index[3],
                'level': index[4],
                'position': index[5],
                'pk_product': row['seqproduto'],
                'description': row['desccompleta'],
                'stock': row['qtdatual'],
                'qtd_packing': row['qtdembcarga'],
                'qtd_order': row['qtdembsolcarga'],
                'qtd_selected': 0.0,
                'pk_customer': index[6],
                'unity': row['embalagem'],
                'weight': row['peso'],
                'volume': row['volume_m3']
            }

    def _save_user_products(self, user_products):
        for index, row in user_products.iterrows():
            data = self._get_iterrow(index, row)
            pk = f'user:{USER_NAME},charge:{data["charge"]},order:{data["pk_order"]},product={data["pk_product"]}'
            # Assumes the default UTF-8
            hash_object = hashlib.sha256(pk.encode())
            data['pk_user_products'] = hash_object.hexdigest()
            data['side'] = 'E' if (int(data['tower']) % 2) == 0 else 'D'
            obj_data = UserProducts(**data)
            obj_data.save()

    @property
    def fractional_products(self):
        self._get_products_data_frame()
        if self.result['status']['sttCode'] == 200:
            group = self._filter_user_product()
            user_products = group.sum() if group is not None else group
            self._save_user_products(user_products)
        else:
            return self.result
