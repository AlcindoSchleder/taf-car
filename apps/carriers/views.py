# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from data_control.products import ProductDataControl
from django.contrib.auth import logout
from apps.home.models import Cars, CarsBoxes
import apps


class CarriersPageView(TemplateView):
    template_name = 'carriers/carriers.html'
    df = None
    flag_validate = True
    pdc = None

    @staticmethod
    def _reset_car():
        apps.USER_NAME = None
        apps.USER_DATA = None
        apps.CAR_PREPARED = False
        apps.CAR_COLLECT_PRODUCTS = False
        apps.CAR_LEVELS = 2
        apps.CAR_BOXES_LEVEL = 5
        apps.CAR_BOXES = {}
        apps.DATA_FRAME = None
        apps.BOX_MAX_WEIGHT = 30000
        apps.BOX_MAX_VOLUME = 0.072
        apps.VOLUME_PERCENT = 30
        apps.USER_PERMISSIONS = []

    def collect_products(self, request) -> dict:
        response = None
        msg_validate = ''
        if apps.CAR_COLLECT_PRODUCTS:
            self.pdc = ProductDataControl()
            response = self.pdc.fractional_products
            if type(response) == 'dict':
                self._reset_car()
                logout(request)
                response['result_to'] = 'collect_products'
                msg_validate = response['status']['sttMsgs'] + ' - ' + response['url']
        else:
            apps.prepare_boxes()
        return {
            "response": response,
            "msg_validate": msg_validate,
            "car_id": apps.CAR_ID,
            "prepared": apps.CAR_PREPARED,
            "loaded": apps.CAR_COLLECT_PRODUCTS,
            "boxes": apps.CAR_BOXES,
        }

    def get(self, request, *args, **kwargs):
        # Load cargo products to pandas.
        if not apps.CAR_PREPARED:
            if request.GET.get('prepared') and request.GET.get('prepared').lower() in ['true', '1']:
                apps.CAR_PREPARED = True
            else:
                apps.CAR_PREPARED = False
        try:
            param = self.collect_products(request)
            # TODO: 1) Order DataFrame by columns left (odd) and right (even)
            #       2) start mqtt to displays boxes
        except Exception as e:
            return render(request, self.template_name, {'msg_validate': e})
        return render(request, self.template_name, param)

    def _validate_boxes(self, data: dict) -> dict:
        self.flag_validate = True
        self.msg_validate = ''
        for key in data:
            value = data[key]
            if value[0] == '' or key == 'csrfmiddlewaretoken':
                continue
            else:
                box_level = key[1]
                box_box = key[2]
                if list(data.values()).count(value) > 1:
                    self.flag_validate = False
                    self.msg_validate = 'Duplicidade de caçambas detectada '
                    self.msg_validate += f'(nível: {box_level} posição: {box_box} código: {value}).'
                    break
                apps.CAR_BOXES[str(box_level)][str(box_box)] = value[0]

        return {
            "car_id": apps.CAR_ID,
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
                    car_box.fisical_box_id = apps.CAR_BOXES[level][box]
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
            data['msg_validate'] = self.msg_validate
            return render(request, self.template_name, data)
