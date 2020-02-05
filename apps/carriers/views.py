# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render
from data_control.products import ProductDataControl
from .models import CarriersProducts

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
        response = pdc.get_products_data_frame()
        if response['status']['sttCode'] == 200:
            df = pdc.data_frame
            self.save_data(df)

        # TODO: filter DataFrame data from all user permissions
        #       group DataFrame by rua, predio, local,
        #       order DataFrame by columns left (odd) and right (even)
        return render(request, self.template_name, {"levels": levels, "boxes": boxes, "response": response})
