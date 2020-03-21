# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render
from urllib.parse import urlparse


class DisplayPageView(TemplateView):
    template_name = 'display/display.html'
    VALID_DISPLAY = ['e' + '21', 'e' + '22', 'e' + '23', 'e' + '24', 'e' + '25',
                     'e' + '11', 'e' + '12', 'e' + '13', 'e' + '14', 'e' + '15']

    def validate_ids(self, request):
        car_id = int(request.GET.get('car_id'))
        display_id = request.GET.get('display_id')
        if (display_id == '') and (car_id < 1):
            raise Exception('Erro: Não posso mostrar o display sem estar vinculado ao carro e o seu nome!')
        if display_id not in self.VALID_DISPLAY:
            raise Exception(f'Display name must be a value between e2[1-5] and e1[1-5]')
        return car_id, display_id

    def get(self, request, *args, **kwargs):
        display_id = kwargs.get('display_id')
        car_id = kwargs.get('car_id')
        # # car_id, display = self.validate_ids(request)
        # display = 'e' + '21'
        # car_id = 1
        # display_id = display if display_id is None else display_id

        site_uri = urlparse(request.build_absolute_uri())
        host = f'{site_uri.scheme}://{site_uri.netloc}'
        request.session['display_id'] = display_id
        request.session['car_id'] = car_id

        params = {
            'car_id': car_id,
            'display_id': display_id,
            'host': host
        }
        return render(request, self.template_name, params)
