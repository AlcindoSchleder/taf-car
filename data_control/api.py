# -*- coding: utf-8 -*-
import requests
import json
from apps import result_dict
from contrib.check import CheckHost


class ApiHostAccess:

    END_POINTS = {}
    proto = 'http'
    port = 5180

    def __init__(self, end_points: dict):
        self.END_POINTS = {}
        if len(end_points) > 0:
            for endpoint in end_points:
                self.END_POINTS[endpoint] = end_points[endpoint]

    def get_data(self, endpoint: str) -> dict:
        result = result_dict()
        check = CheckHost()
        host = check.check_hosts()
        if not host:
            result['status']['sttCode'] = 404
            result['status']['sttMsgs'] = 'Error: Host(s) not found!'
            return result
        url = f'{self.proto}://{host}:{self.port}{self.END_POINTS[endpoint]}'
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(url, headers=headers)
            result['status']['sttCode'] = response.status_code
            result['data'] = json.loads(response.content.decode('utf-8'))
        except Exception as e:
            result['status']['sttCode'] = 500
            result['status']['sttMsgs'] = f'Erro ao ler os dados do usuário no E.R.P.! - {e}'
        return result

    def set_end_points(self, end_points: dict) -> None:
        self.END_POINTS = {}
        for endpoint in end_points:
            self.END_POINTS[endpoint] = end_points[endpoint]
