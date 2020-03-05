# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from data_control.products import ProductDataControl
from apps.home.models import Cars, CarsBoxes
from apps.carriers.models import CarriersCars
from urllib.parse import urlparse
import apps


class CarriersPageView(TemplateView):
    template_name = 'carriers/carriers.html'
    df = None
    flag_validate = True
    pdc = None

    @staticmethod
    def _reset_car():
        apps.USER_NAME = None
        apps.USER_DATA = None
        apps.CAR_PREPARED = False
        apps.CAR_COLLECT_PRODUCTS = False
        apps.CAR_LEVELS = 2
        apps.CAR_BOXES_LEVEL = 5
        apps.CAR_BOXES = {}
        apps.DATA_FRAME = None
        apps.BOX_MAX_WEIGHT = 30000
        apps.BOX_MAX_VOLUME = 0.072
        apps.VOLUME_PERCENT = 30
        apps.USER_PERMISSIONS = []

    def collect_products(self, request) -> dict:
        response = None
        msg_validate = ''

        if apps.CAR_COLLECT_PRODUCTS:
            self.pdc = ProductDataControl()
            response = self.pdc.fractional_products
            if type(response) == 'dict':
                if response['status']['sttCode'] != 200:
                    self._reset_car()
                    logout(request)
                    response['result_to'] = 'collect_products'
                    msg_validate = response['status']['sttMsgs'] + ' - ' + response['url']
                else:
                    # TODO: Verificar o que vem em data para mostrar no render dos displays ou mensagens dos displays
                    data = self.pdc.product_data()
        else:
            apps.prepare_boxes()
        return {
            "response": response,
            "msg_validate": msg_validate,
            "car_id": apps.CAR_ID,
            "car_prepared": int(apps.CAR_PREPARED),
            "car_collect_products": int(apps.CAR_COLLECT_PRODUCTS),
            "boxes": apps.CAR_BOXES,
        }

    def get(self, request, *args, **kwargs):
        # Load cargo products to pandas.
        site_uri = urlparse(request.build_absolute_uri())
        host = f'{site_uri.scheme}://{site_uri.netloc}'
        flag = 'car_prepared'
        apps.CAR_PREPARED = bool(int(request.GET.get(flag))) if request.GET.get(flag) else False
        # apps.CAR_PREPARED = bool(apps.CAR_PREPARED)
        flag = 'car_collect_products'
        apps.CAR_COLLECT_PRODUCTS = bool(int(request.GET.get(flag))) if request.GET.get(flag) else False
        # apps.CAR_COLLECT_PRODUCTS = bool(apps.CAR_COLLECT_PRODUCTS)
        try:
            apps.CAR_ID = request.session.get('car_id')
            param = self.collect_products(request)
            if param['message'] == '':
                param['message'] = request.session.get('message') if request.session.get('message') else ''
            param['host'] = host
        except Exception as e:
            return render(request, self.template_name, {'message': e})
        return render(request, self.template_name, param)

    def post(self, request):
        apps.CAR_ID = request.session.get('car_id', 0)
        if apps.CAR_ID <= 0:
            message = 'Erro ao Alocar as Caixas: Identificação do Carro não foi Fornecida!'
            return redirect(apps.get_redirect_url('home:home', message=message))

        res, msg = CarsBoxes.save_data(dict(request.POST))
        apps.CAR_PREPARED = res
        if res:
            msg = 'Configuração das Caçambas realizada com sucesso!!'
            data = {'car_id': apps.CAR_ID, 'car_prepared': True, 'message': msg}
            return redirect(apps.get_redirect_url('home:home', params=data))
        else:
            data = {'car_id': apps.CAR_ID, 'car_prepared': False, 'message': msg}
            return render(request, self.template_name, data)
