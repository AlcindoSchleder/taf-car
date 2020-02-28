# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render
from urllib.parse import urlparse


class DisplayPageView(TemplateView):
    template_name = 'display/display.html'

    @staticmethod
    def validate_ids(request):
        car_id = request.session.get('car_id', 0) \
            if request.session.get('car_id', 0) > 0 \
            else int(request.GET.get('car_id'))
        display_id = request.session.get('display_id', '') \
            if request.session.get('display_id', '') != '' \
            else request.GET.get('display_id')
        return car_id, display_id, (display_id != '') and (car_id > 0)

    def get(self, request, *args, **kwargs):
        car_id, display_id, flag_validate = self.validate_ids(request)
        if not flag_validate:
            raise Exception('Erro: Não posso mostrar o display sem estar vinculado ao carro e o seu nome!')
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
