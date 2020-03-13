# -*- coding: utf-8 -*-
import os
import requests
import json
import apps
# import pandas as pd
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from urllib.parse import urlparse
from .models import CarsBoxes
from data_control.products import ProductDataControl


class HomePageView(TemplateView):
    template_name = 'home/index.html'
    host = None

    def _send_message(self, command_type, display, message):
        result = apps.result_dict()
        api = self.host + '/api/mqtt/send_message/'
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
        pk_cars_gt = int(f'{apps.CAR_ID}10')
        pk_cars_lt = int(f'{apps.CAR_ID}{apps.CAR_LEVELS}{apps.CAR_BOXES_LEVEL}')
        boxes = CarsBoxes.objects.filter(pk__range=(pk_cars_gt, pk_cars_lt), fisical_box_id__isnull=False)
        apps.CAR_PREPARED = boxes.count() == (apps.CAR_LEVELS * apps.CAR_BOXES_LEVEL)
        if apps.CAR_PREPARED:
            for box in boxes:
                display_id = box.box_name
                box_id = box.fisical_box_id
                res = self._send_message('control', display_id, box_id)
                if res['status']['sttCode'] != 200:
                    return False, res['status']['sttMsgs']
        return apps.CAR_PREPARED, ''

    def get(self, request, *args, **kwargs):
        # proto = 'https://'
        # if request.META['SERVER_PROTOCOL'] and request.META['SERVER_PROTOCOL'][0:5] == 'HTTP/':
        #     proto = 'http://'
        # server = proto + request.META['HTTP_HOST']
        message = ''
        apps.DATA_FRAME = None
        apps.CAR_ID = int(request.session.get('car_id', 0))
        site_uri = urlparse(request.build_absolute_uri())
        self.host = f'{site_uri.scheme}://{site_uri.netloc}'
        # host = site_uri.netloc
        if len(request.GET) > 0:
            if apps.CAR_ID < 1:
                apps.CAR_ID = int(request.GET.get('car_id')) if request.GET.get('car_id') else 0
            apps.CAR_PREPARED = bool(request.GET.get('car_prepared')) \
                if request.GET.get('car_prepared') else False
            if not apps.CAR_PREPARED:
                apps.CAR_PREPARED, message = self._check_allocation_boxes()
            apps.CAR_COLLECT_PRODUCTS = True if apps.CAR_PREPARED else False
            message = request.GET.get('message') if request.GET.get('message') else ''
            request.session['car_id'] = apps.CAR_ID
        params = {
            'car_id': apps.CAR_ID,
            'car_prepared': int(apps.CAR_PREPARED),
            'car_collect_products': int(apps.CAR_COLLECT_PRODUCTS),
            'host': self.host,
            'message': message,
        }
        if apps.CAR_PREPARED and not request.user.is_authenticated:
            return redirect(apps.get_redirect_url('login:login', params=params))
        if apps.CAR_PREPARED and request.user.is_authenticated:
            return redirect(apps.get_redirect_url('carriers:carriers', params=params))
        return render(request, self.template_name, params)


class HomeTestsView(TemplateView):

    def get(self, request, *args, **kwargs):

        def as_dict(qs):
            return [item for item in qs]

        def calc_volume(x):
            return (x['altura'] / 100) * (x['largura'] / 100) * (x['profundidade'] / 100)

        def get_side(x):
            return 'E' if (x['nropredio'] % 2) == 0 else 'D'

        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        header = os.path.join(base_dir, 'templates/home/http_header.html')
        footer = os.path.join(base_dir, 'templates/home/http_footer.html')
        with open(header, "r") as fd:
            header = fd.read()
            fd.close()
        with open(footer, "r") as fd:
            footer = fd.read()
            fd.close()

        apps.CAR_ID = request.session['car_id']
        apps.CAR_PREPARED = 1
        apps.CAR_COLLECT_PRODUCTS = 1
        apps.USER_NAME = request.user.username
        # res = apps.result_dict()
        # if res.get('status') and res['status'].get('sttCode'):
        #     code = res['status'].get('sttCode')
        #     res['status']['sttMsgs'] = f'Encontrou sttCode {code}'
        pdc = ProductDataControl()

        # res = pdc.load_all_charges()     # TESTED OK
        res, df = pdc.load_boxes_from_operator()

        # df = pd.DataFrame(res)
        # file_name = "./temp/carga_produtos.csv"
        # df = pd.read_csv(file_name, delimiter=',', encoding='latin1')
        # df = df[df['tipseparacao'] == 'CO']
        # df['status'] = 'L'
        # df['volume'] = df.apply(calc_volume, axis=1)
        # df['side'] = df.apply(get_side, axis=1)
        # df = df[FILTER_PROD]
        # df.sort_values(COLLECT_SORT, inplace=True)

        css_classes = 'table table-sm table-hover'
        res_str = str(res)
        if df is None:
            html = f'{header}\n<pre>\n{res_str}\n</pre>\n{footer}'
            return HttpResponse(html)
        else:
            header += f'<pre>{res_str}</pre>\n'
            return HttpResponse(header + df.to_html(classes=css_classes, float_format='%.4f', decimal=',') + footer)

