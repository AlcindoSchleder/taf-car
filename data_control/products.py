# -*- coding: utf-8 -*-
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import pandas as pd
from taf_car.settings import API_URLS
import requests
import json


class ProductDataControl:

    END_POINTS = {
        'product': '/tafAPI/product/1.0',
        'product-image': '/tafAPI/product/1.0/code'
    }
    df = None
    host = None
    proto = 'http'
    port = 5180
    url = f'{proto}://%s:{port}'
    result = {
        'status': {
            'sttCode': 200,
            'sttMsgs': '',
        },
        'data': []
    }

    def _check_hosts(self):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """
        self.df = None
        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        for host in API_URLS:
            # Building the command. Ex: "ping -c 1 host"
            command = ['ping', param, '1', API_URLS[host]]
            if subprocess.call(command) == 0:
                return API_URLS[host]
        return None

    def _get_all_products(self):
        self.host = self._check_hosts()
        if not self.host:
            self.result['status']['sttCode'] = 404
            self.result['status']['sttMsgs'] = 'Error: Host(s) not found!'
            return self.result
        self.url = self.url.format(self.host)
        headers = {'Content-Type': 'application/json'}
        self.result['status']['sttCode'] = 200
        self.result['status']['sttMsgs'] = ''
        try:
            response = requests.get(self.url, headers=headers)
            self.result['status']['sttCode'] = response.status_code
            self.result['data'] = json.loads(response.content.decode('utf-8'))
        except Exception as e:
            self.result['status']['sttCode'] = 500
            self.result['status']['sttMsgs'] = e.__str__()
        return self.result

    def get_products_data_frame(self) -> dict:
        self._get_all_products()
        if self.result['status']['sttCode'] == 200 and self.result['data'] is not None:
            self.df = pd.DataFrame(self.result['data'])
        self.result['data'] = []
        return self.result

    @property
    def data_frame(self):
        return self.df
