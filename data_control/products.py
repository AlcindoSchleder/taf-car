# -*- coding: utf-8 -*-
import socket
import time
import pandas as pd
from taf_car.settings import API_URLS
from apps import RESULT_DICT
import requests
import json


class ProductDataControl:

    END_POINTS = {
        'all_products': '/tafApi/product/1.0/',
        'product': '/tafApi/product/1.0/%d',
        'product-image': '/tafAPI/product/1.0/pk/%s'
    }
    df = None
    host = None
    _PROTO = 'http'
    _PORT = 5180
    url = f'{_PROTO}://%s:{_PORT}%s'
    result = RESULT_DICT
    _TIMEOUT = 1

    def _check_hosts(self):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """
        self.df = None
        # Option for the number of packets as a function of
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self._TIMEOUT)
        idx = 0
        while idx < len(API_URLS):
            try:
                s.connect((API_URLS[idx], int(self._PORT)))
                s.shutdown(socket.SHUT_RDWR)
                return API_URLS[idx]
            except:
                continue
            finally:
                idx += 1
                s.close()
        return None

    def _get_all_products(self):
        self.host = self._check_hosts()
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
        self.result['data'] = []
        return self.result

    @property
    def data_frame(self):
        return self.df
