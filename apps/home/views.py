# -*- coding: utf-8 -*-
import apps
from django.views.generic import TemplateView
from django.shortcuts import render
from urllib.parse import urlparse
from .models import CarsBoxes


class HomePageView(TemplateView):
    template_name = 'home/index.html'

    def _check_allocation_boxes(self):
        car = CarsBoxes.objects.filter(pk=apps.CAR_ID)
        return car.count() > 0

    def get(self, request, *args, **kwargs):
        # proto = 'https://'
        # if request.META['SERVER_PROTOCOL'] and request.META['SERVER_PROTOCOL'][0:5] == 'HTTP/':
        #     proto = 'http://'
        # server = proto + request.META['HTTP_HOST']
        message = ''
        apps.DATA_FRAME = None
        apps.CAR_ID = request.session.get('car_id', 0)
        site_uri = urlparse(request.build_absolute_uri())
        host = f'{site_uri.scheme}://{site_uri.netloc}'
        # host = site_uri.netloc
        if len(request.GET) > 0:
            if apps.CAR_ID < 1:
                apps.CAR_ID = int(request.GET.get('car_id')) if request.GET.get('car_id') else 0
            apps.CAR_PREPARED = bool(request.GET.get('car_prepared')) \
                if request.GET.get('car_prepared') else False
            apps.CAR_COLLECT_PRODUCTS = True if apps.CAR_PREPARED else False
            message = request.GET.get('message') if request.GET.get('message') else ''
            request.session['car_id'] = apps.CAR_ID
            request.session['host'] = host
            apps.CAR_PREPARED = self._check_loaded_boxes()
        params = {
            'car_id': apps.CAR_ID,
            'car_prepared': int(apps.CAR_PREPARED),
            'car_collect_products': int(apps.CAR_COLLECT_PRODUCTS),
            'host': host,
            'message': message,
        }
        return render(request, self.template_name, params)
