# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render
import apps


class HomePageView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        # proto = 'https://'
        # if request.META['SERVER_PROTOCOL'] and request.META['SERVER_PROTOCOL'][0:5] == 'HTTP/':
        #     proto = 'http://'
        # server = proto + request.META['HTTP_HOST']

        apps.CAR_ID = request.GET.get('carid') if request.GET.get('carid') else 0
        apps.CAR_LOADED = request.GET.get('loaded') if request.GET.get('loaded') else False
        return render(request, self.template_name, {'carid': apps.CAR_ID, 'loaded': apps.CAR_LOADED})
