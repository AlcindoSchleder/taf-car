# -*- coding: utf-8 -*-
import apps
from django.views.generic import TemplateView
from django.shortcuts import render
from urllib.parse import urlparse


class HomePageView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        # proto = 'https://'
        # if request.META['SERVER_PROTOCOL'] and request.META['SERVER_PROTOCOL'][0:5] == 'HTTP/':
        #     proto = 'http://'
        # server = proto + request.META['HTTP_HOST']
        apps.DATA_FRAME = None
        apps.CAR_ID = request.session.get('car_id', 0)
        site_uri = urlparse(request.build_absolute_uri())
        host = f'{site_uri.scheme}://{site_uri.netloc}'
        # host = site_uri.netloc
        if len(request.GET) > 0 and int(apps.CAR_ID) < 1:
            apps.CAR_ID = int(request.GET.get('car_id')) if request.GET.get('car_id') else 0
            apps.CAR_PREPARED = request.session.get('car_prepared', False)
            request.session['car_id'] = apps.CAR_ID
            request.session['car_prepared'] = apps.CAR_PREPARED
            request.session['host'] = host
        params = {
            'car_id': apps.CAR_ID,
            'car_prepared': apps.CAR_PREPARED,
            'host': host
        }
        return render(request, self.template_name, params)
