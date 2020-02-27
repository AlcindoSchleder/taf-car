# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render


class DisplayPageView(TemplateView):
    template_name = 'display/display.html'

    @staticmethod
    def validate_ids(request, display_id, car_id):
        car_id = car_id if car_id > 0 else int(request.GET.get('car_id'))
        display_id = display_id if display_id != '' else request.GET.get('display_id')
        return (display_id != '') and (car_id > 0)

    def get(self, request, *args, **kwargs):
        display_id = request.session.get('display_id', '')
        car_id = request.session.get('car_id', 0)
        if not self.validate_ids(request, display_id, car_id):
            raise Exception('Erro: Não posso mostrar o display sem estar vinculado ao carro e o seu nome!')
        request.session['display_id'] = display_id
        request.session['car_id'] = car_id

        show_display = ''
        if 'show_display' in request.GET.keys():
            show_display = request.GET.get('show_display')
        params = {
            'car_id': car_id,
            'display_id': display_id,
            'show_display': show_display
        }
        return render(request, self.template_name, params)
