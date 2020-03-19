# -*- coding: utf-8 -*-
import os
import apps
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from urllib.parse import urlparse
from .models import Cars, CarsBoxes
from data_control.products import ProductDataControl
from .forms import ClassificationChargesForm


class HomePageView(TemplateView):
    template_name = 'home/index.html'
    host = None

    def _send_message(self, command_type, display, message):
        pass

    def get(self, request, *args, **kwargs):
        apps.CAR_ID = kwargs.get('car_id')
        request.session['car_id'] = apps.CAR_ID

        message = ''
        params = {
            'car_id': apps.CAR_ID,
            'message': message,
            'form': ClassificationChargesForm,
        }

        return render(request, self.template_name, params)


class OperationPageView(TemplateView):
    template_name = 'home/operation.html'
    host = None

    def get(self, request, *args, **kwargs):
        apps.CAR_ID =  kwargs.get('car_id')
        request.session['car_id'] = apps.CAR_ID
        try:
            car = Cars.objects.get(pk_cars=apps.CAR_ID)
        except ObjectDoesNotExist:
            message = f'O carro ({apps.CAR_ID}) não está na nossa base de dados'
            return render(request, self.template_name, {'message': message})

        site_uri = urlparse(request.build_absolute_uri())
        self.host = f'{site_uri.scheme}://{site_uri.netloc}'

        apps.CAR_PREPARED = bool(request.GET.get('car_prepared')) \
            if request.GET.get('car_prepared') else False
        apps.CAR_COLLECT_PRODUCTS = True if apps.CAR_PREPARED else False
        message = request.GET.get('message') if request.GET.get('message') else ''

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

        type_test = kwargs.get('type')
        apps.CAR_ID = kwargs.get('car_id')

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

        apps.CAR_PREPARED = 1
        apps.CAR_COLLECT_PRODUCTS = 1
        apps.USER_NAME = request.user.username

        res = apps.result_dict()
        if type_test not in ['load_boxes', 'get_charges', 'generate_boxes']:
            res['status']['sttCode'] = 404
            res['status']['sttMsg'] = 'Type param must be "load_boxes" or "get_charges"'
            res_str = str(res)
            html = f'{header}\n<pre>\n{res_str}\n</pre>\n{footer}'
            return HttpResponse(html)

        pdc = ProductDataControl()
        df = None
        if type_test == 'generate_boxes':
            res, df = pdc.load_boxes_from_operator()
        elif type_test == 'load_boxes':
            if pdc.get_allocation_boxes():
                res['status']['sttCode'] = 200
                res['status']['sttMsgs'] = 'Ok... Caçambas Alocadas!'
            else:
                res['status']['sttCode'] = 404
                res['status']['sttMsgs'] = 'Caçambas ainda não foram alocadasAlocadas!'

        css_classes = 'table table-striped'
        res_str = str(res)
        if df is None:
            html = f'{header}\n<pre>\n{res_str}\n</pre>\n{footer}'
            return HttpResponse(html)
        else:
            header += f'<pre>{res_str}</pre>\n'
            # return HttpResponse(header + df.to_html(classes=css_classes, float_format='%.4f', decimal=',') + footer)
            return HttpResponse(header + df.to_html(classes=css_classes, decimal=',') + footer)

