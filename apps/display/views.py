# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render


class DisplayPageView(TemplateView):
    template_name = 'display/display.html'

    def get(self, request, *args, **kwargs):
        car_id = int(request.GET.get('car_id'))
        display = request.GET.get('display_id')

        show_display = ''
        if 'show_display' in request.GET.keys():
            show_display = request.GET.get('show_display')
        params = {
            'car_id': car_id,
            'display_id': display,
            'show_display': show_display
        }
        return render(request, self.template_name, params)
