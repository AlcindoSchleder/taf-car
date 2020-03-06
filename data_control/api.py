# -*- coding: utf-8 -*-
import requests
import json
from apps import result_dict
from contrib.check import CheckHost


class ApiHostAccess:

    END_POINTS = {}
    host = None
    proto = 'http'
    port = 5180
    url = f'{proto}://%s:{port}%s'
    result = None

    def __init__(self, end_points: dict):
        self.result = result_dict()
        self.END_POINTS = {}
        if len(end_points) > 0:
            for endpoint in end_points:
                self.END_POINTS[endpoint] = end_points[endpoint]

    def get_data(self, endpoint: str) -> dict:
        check = CheckHost()
        self.host = check.check_hosts()
        if not self.host:
            self.result['status']['sttCode'] = 404
            self.result['status']['sttMsgs'] = 'Error: Host(s) not found!'
            return self.result
        self.url = self.url % (self.host, self.END_POINTS[endpoint])
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

    def set_end_points(self, end_points: dict) -> None:
        self.END_POINTS = {}
        for endpoint in end_points:
            self.END_POINTS[endpoint] = end_points[endpoint]
