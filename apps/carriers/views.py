# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from data_control.products import ProductDataControl
from .models import CarriersProducts
import apps
pdc = ProductDataControl()


class CarriersPageView(TemplateView):
    template_name = 'carriers/carriers.html'

    def save_data(self, df) -> bool:
        for index, row in df.iterrows():
            data = CarriersProducts(**row)
            data.save()
        return True

    def get(self, request, *args, **kwargs):
        levels = [2, 1]
        boxes = [1, 2, 3, 4, 5]
        # Load cargo products to pandas.
        load_boxes = request.GET.get('load_boxes') if request.GET.get('load_boxes') else False
        response = False
        if not load_boxes:
            response = pdc.get_products_data_frame()
            if response['status']['sttCode'] == 200:
                df = pdc.data_frame
                self.save_data(df)

        param = {
            "levels": levels,
            "boxes": boxes,
            "response": response,
            "carid": apps.CAR_ID,
            "loadbox": load_boxes,
            "boxesid": apps.CAR_BOXES,
        }
        # TODO: filter DataFrame data from all user permissions
        #       group DataFrame by rua, predio, local,
        #       order DataFrame by columns left (odd) and right (even)
        return render(request, self.template_name, param)

    def post(self, request, *args, **kwargs):
        data = request.POST
        # TODO: Validate form carriers and save data
        apps.CAR_LOADED = True
        return redirect('/', carid=apps.CAR_ID, loaded=apps.CAR_LOADED)
