# -*- coding: utf-8 -*-
import pandas as pd
from taf_car.settings import API_URLS
from apps import RESULT_DICT, USER_NAME, USER_PERMISSIONS
from contrib.check import CheckHost
from apps.login.models import UsersOperatorsPermissions
import requests
import json


class ProductDataControl:

    END_POINTS = {
        'all_products': '/tafApi/product/1.0/',
        'product': '/tafApi/product/1.0/%d',
        'product-image': '/tafAPI/product/1.0/pk/%s'
    }
    FILTER_PROD = [
        'seqproduto', 'desccompleta', 'qtdatual', 'qtdembcarga', 'qtdembsolcarga',
        'qtdembsepcarga', 'nropedvenda', 'embalagem', 'pesobruto', 'pesoliquido',
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
        'seqproduto'
    ]

    df = None
    host = None
    _PROTO = 'http'
    _PORT = 5180
    url = f'{_PROTO}://%s:{_PORT}%s'
    result = RESULT_DICT
    _TIMEOUT = 3.5

    def _get_all_products(self):
        check = CheckHost(API_URLS)
        self.host = check.check_hosts()
        if not self.host:
            self.result['status']['sttCode'] = 404
            self.result['status']['sttMsgs'] = 'Error: Host(s) not found!'
            return self.result
        self.url = self.url %(self.host, self.END_POINTS['all_products'])
        self.result['url'] = self.url
        headers = {'Content-Type': 'application/json'}
        self.result['status']['sttCode'] = 200
        self.result['status']['sttMsgs'] = ''
        try:
            response = requests.get(self.url, headers=headers)
            self.result['status']['sttCode'] = response.status_code
            self.result['data'] = json.loads(response.content.decode('utf-8'))
        except Exception as e:
            self.result['status']['sttCode'] = 500
            self.result['status']['sttMsgs'] = f'Error on read ERP products: [{e}]'
        return self.result

    def get_products_data_frame(self) -> dict:
        self._get_all_products()
        if self.result['status']['sttCode'] == 200 and self.result['data'] is not None:
            self.df = pd.DataFrame(self.result['data']['records'])
        # self.result['data'] = []
        return self.result

    def filter_user_product(self):
        df = self.df[self.df['tipseparacao'].isin(USER_PERMISSIONS)].copy()
        prod = df[self.FILTER_PROD].copy()
        prod['peso'] = prod['qtdembsolcarga'] * prod['pesobruto']
        prod['volume_m3'] = prod['qtdembcarga'] * (prod['altura'] * prod['largura'] * prod['profundidade']) / 1000000
        return prod.groupby(by=self.GROUP_BY_FIELDS)

    @property
    def data_frame(self):
        group = self.filter_user_product()
        return group.sum() if group is not None else None
