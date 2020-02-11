# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from data_control.products import ProductDataControl
from .models import CarriersProducts
from apps.home.models import Cars, CarsBoxes
import apps

pdc = ProductDataControl()


class CarriersPageView(TemplateView):
    template_name = 'carriers/carriers.html'
    df = None
    flag_validate = True

    def save_charge_products(self) -> bool:
        if not self.df:
            return False
        for index, row in self.df.iterrows():
            data = CarriersProducts(**row)
            data.save()
        return True

    def get(self, request, *args, **kwargs):
        # Load cargo products to pandas.
        response = False
        if len(kwargs) <= 0:
            if request.GET.get('prepared') and request.GET.get('prepared').lower() in ['true', '1']:
                apps.CAR_PREPARED = True
            else:
                apps.CAR_PREPARED = False
        if apps.CAR_LOADED:
            response = pdc.get_products_data_frame()
            if response['status']['sttCode'] == 200:
                self.df = pdc.data_frame
                self.save_charge_products()
                apps.CAR_LOADED = True
        else:
            apps.prepare_boxes()

        param = {
            "response": response,
            "carid": apps.CAR_ID,
            "prepared": apps.CAR_PREPARED,
            "boxes": apps.CAR_BOXES,
        }
        # TODO: filter DataFrame data from all user permissions
        #       group DataFrame by rua, predio, local,
        #       order DataFrame by columns left (odd) and right (even)
        return render(request, self.template_name, param)

    def _validate_boxes(self, data: dict) -> dict:
        self.flag_validate = True
        self.msg_validate = ''
        for key in data:
            value = data[key]
            if value == '' or key == 'csrfmiddlewaretoken':
                continue
            else:
                box_level = key[1]
                box_box = key[2]
                if list(data.values()).count(value) > 1:
                    self.flag_validate = False
                    self.msg_validate = 'Duplicidade de caçambas detectada '
                    self.msg_validate += f'(nível: {box_level} posição: {box_box} código: {value}).'
                    break
                apps.CAR_BOXES[str(box_level)][str(box_box)] = value

        return {
            "carid": apps.CAR_ID,
            "prepared": apps.CAR_PREPARED,
            "boxes": apps.CAR_BOXES,
            "flag_validate": self.flag_validate,
            "msg": self.msg_validate,
        }

    def _save_data(self):
        if not self.flag_validate:
            return False
        for level in apps.CAR_BOXES:
            for box in apps.CAR_BOXES[level]:
                pk = int(str(apps.CAR_ID) + str(level) + str(box))
                try:
                    car = Cars.objects.get(pk=apps.CAR_ID)
                    car_box = CarsBoxes()
                    car_box.pk_carboxes = pk
                    car_box.box_name = box
                    car_box.fisical_box_id = apps.CAR_BOXES[level][box][0]
                    car_box.level = level
                    car_box.box = box
                    car_box.weight = 0
                    car_box.volume = 0
                    car_box.fk_cars = car
                    car_box.save()
                except Exception as e:
                    self.msg_validate = f'Error when save carboxes! ({e})'
                    return False

        return True

    def post(self, request):
        data = self._validate_boxes(dict(request.POST))
        if data['flag_validate']:
            apps.CAR_PREPARED = True
            if self._save_data():
                return redirect('home:home')
            else:
                data['msg_validate'] = self.msg_validate
                return render(request, self.template_name, data)
        else:
            return render(request, self.template_name, data)
