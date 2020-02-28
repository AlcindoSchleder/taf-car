# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render
from urllib.parse import urlparse


class DisplayPageView(TemplateView):
    template_name = 'display/display.html'
    VALID_DISPLAY = ['e21', 'e22', 'e23', 'e24', 'e25', 'e11', 'e12', 'e13', 'e14', 'e15']

    def validate_ids(self, request):
        car_id = int(request.GET.get('car_id'))
        display_id = request.GET.get('display_id')
        if (display_id == '') and (car_id < 1):
            raise Exception('Erro: Não posso mostrar o display sem estar vinculado ao carro e o seu nome!')
        if display_id not in self.VALID_DISPLAY:
            raise Exception(f'Display name must be a value between e2[1-5] and e1[1-5]')
        return car_id, display_id

    def get(self, request, *args, **kwargs):
        car_id, display_id = self.validate_ids(request)
        site_uri = urlparse(request.build_absolute_uri())
        host = f'{site_uri.scheme}://{site_uri.netloc}'
        request.session['display_id'] = display_id
        request.session['car_id'] = car_id

        show_display = ''
        if 'show_display' in request.GET.keys():
            show_display = request.GET.get('show_display')
        params = {
            'car_id': car_id,
            'display_id': display_id,
            'show_display': show_display,
            'host': host
        }
        return render(request, self.template_name, params)
