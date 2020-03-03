# -*- coding: utf-8 -*-
import requests
import json
import apps
from django.views.generic import TemplateView
from django.shortcuts import render
from urllib.parse import urlparse
from .models import CarsBoxes


class HomePageView(TemplateView):
    template_name = 'home/index.html'
    host = None

    def _send_message(self, command_type, display, message):
        result = apps.result_dict()
        api = self.host + '/api/mqtt/send_message/';
        api_name = f'{command_type} of displays'
        command = {
            'type': command_type,
            'car_id': apps.CAR_ID,
            'display': display,
            'message': message
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(api, headers=headers, params=command)  # Call API with parameters on url
            result['status']['sttCode'] = response.status_code
            result['data'] = json.loads(response.content.decode('utf-8'))
        except Exception as e:
            result['status']['sttCode'] = 500
            result['status']['sttMsgs'] = f'Error on API {api_name} ({api}): [{e}]'
        return result

    def _check_allocation_boxes(self):
        boxes = CarsBoxes.objects.filter(pk=apps.CAR_ID)
        if boxes.count > 0:
            for box in boxes:
                display_id = box.box_name
                box_id = box.fisical_box_id
                res = self._send_message('control', display_id, box_id)
                if res['status']['sttCode'] != 200:
                    return False, res['status']['sttMsgs']
        return boxes.count() > 0, ''

    def get(self, request, *args, **kwargs):
        # proto = 'https://'
        # if request.META['SERVER_PROTOCOL'] and request.META['SERVER_PROTOCOL'][0:5] == 'HTTP/':
        #     proto = 'http://'
        # server = proto + request.META['HTTP_HOST']
        message = ''
        apps.DATA_FRAME = None
        apps.CAR_ID = request.session.get('car_id', 0)
        site_uri = urlparse(request.build_absolute_uri())
        self.host = f'{site_uri.scheme}://{site_uri.netloc}'
        # host = site_uri.netloc
        if len(request.GET) > 0:
            if apps.CAR_ID < 1:
                apps.CAR_ID = int(request.GET.get('car_id')) if request.GET.get('car_id') else 0
            apps.CAR_PREPARED = bool(request.GET.get('car_prepared')) \
                if request.GET.get('car_prepared') else False
            apps.CAR_COLLECT_PRODUCTS = True if apps.CAR_PREPARED else False
            message = request.GET.get('message') if request.GET.get('message') else ''
            request.session['car_id'] = apps.CAR_ID
            request.session['host'] = self.host
            apps.CAR_PREPARED, message = self._check_allocation_boxes()
        params = {
            'car_id': apps.CAR_ID,
            'car_prepared': int(apps.CAR_PREPARED),
            'car_collect_products': int(apps.CAR_COLLECT_PRODUCTS),
            'host': self.host,
            'message': message,
        }
        return render(request, self.template_name, params)
