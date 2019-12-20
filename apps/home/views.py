# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        # proto = 'https://'
        # if request.META['SERVER_PROTOCOL'] and request.META['SERVER_PROTOCOL'][0:5] == 'HTTP/':
        #     proto = 'http://'
        # server = proto + request.META['HTTP_HOST']
        return render(request, self.template_name)
