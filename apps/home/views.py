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
        apps.DATA_FRAME = None
        if len(request.GET) > 0 and apps.CAR_ID < 1:
            apps.CAR_ID = int(request.GET.get('carid')) if request.GET.get('carid') else 0
            if request.GET.get('prepared') and request.GET.get('prepared').lower() in ['true', '1']:
                apps.CAR_PREPARED = True
            else:
                apps.CAR_PREPARED = False

        return render(request, self.template_name, {'carid': apps.CAR_ID, 'prepared': apps.CAR_PREPARED})
