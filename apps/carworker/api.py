# -*- coding: utf-8 -*-
import requests
import json
from apps import result_dict
from contrib.check import CheckHost


class ApiHostAccess:

    END_POINTS = {
        'all_products': '/tafApi/product/1.0/{pk_charge}',
        'product_barcode': '/tafApi/product/1.0/barcode/{barcode}',
        'product_pk': '/tafApi/product/1.0/pk/{pk_product}'
    }
    proto = 'http'
    port = 5180

    def __init__(self, end_points: dict = None):
        self.set_end_points(end_points)

    def get_data(self, api_name: str, **params) -> dict:
        def check_params(api_url: str):
            for param in params:
                if api_url.find('{' + param + '}') < 0:
                    return False
            return True

        result = result_dict()
        if api_name not in self.END_POINTS:
            result['status']['sttCode'] = 404
            result['status']['sttMsgs'] = f'Error: Entry point for api {api_name} not found!'
            return result
        check = CheckHost()
        host = check.check_hosts()
        if not host:
            result['status']['sttCode'] = 404
            result['status']['sttMsgs'] = 'Error: Host(s) not found!'
            return result

        end_point = self.END_POINTS[api_name].format(**params) \
            if len(params) > 0 and check_params(self.END_POINTS[api_name]) \
            else self.END_POINTS[api_name]

        url = f'{self.proto}://{host}:{self.port}{end_point}'    # mount URL
        result['url'] = url

        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(url, headers=headers)
            result['status']['sttCode'] = response.status_code
            result['data'] = json.loads(response.content.decode('utf-8'))
        except Exception as e:
            result['status']['sttCode'] = 500
            result['status']['sttMsgs'] = \
                f'Error on API {api_name} ({url}) to load products from ERP: [{e}]'

        return result

    def set_end_points(self, end_points: dict = None) -> None:
        if end_points:
            for endpoint in end_points:
                self.END_POINTS[endpoint] = end_points[endpoint]
