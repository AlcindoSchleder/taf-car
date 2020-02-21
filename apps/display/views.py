# -*- coding: utf-8 -*-
import json
import apps
from django.views.generic import TemplateView
from django.shortcuts import render
from decouple import config
from apis.mqtt.mqtt import MqttManager


class DisplayPageView(TemplateView):
    template_name = 'display/display.html'

    MQTT_HOST = config('MQTT_HOST', default='192.168.0.20')
    MQTT_PORT = int(config('MQTT_PORT', default=1883))
    MQTT_CLIENT_ID = config('MQTT_CLIENT_ID', default='iCity_car_v1.0')
    MQTT_USER = config('MQTT_USER')
    MQTT_PASSWORD = config('MQTT_PASSWORD')
    MQTT_TOPIC_BASE = '/taf/car'

    display = None
    show_display = ''

    service = None
    mqtt_payload = ''
    result = apps.RESULT_DICT

    def _on_mqtt_message(self, client, userdata, msg):
        payload = json.dumps(msg.payload)
        if payload['type'] == 'control':
            if payload['message'] == 'display_enabled':
                self.show_display = 'd-none'
            else:
                self.show_display = ''

    def _config_broker(self, car_id: int, display_id: str):
        apps.CAR_ID = car_id
        self.display = display_id
        s = str(apps.CAR_ID).rjust(4, '0')
        self.MQTT_TOPIC_BASE = f'/taf/car{s}'
        self.service = MqttManager(
            self.MQTT_HOST,
            self.MQTT_PORT,
            self.MQTT_TOPIC_BASE,
            self.MQTT_USER,
            self.MQTT_PASSWORD
        )
        self.service.on_message = self._on_mqtt_message
        self.service.subscribe(self.display)

    def get(self, request, *args, **kwargs):
        # self._config_broker(
        #     int(request.GET.get('car_id')), request.GET.get('display_id')
        # )
        # apps.CAR_ID = int(request.GET.get('car_id'))
        # self.display = request.GET.get('display_id')
        # show_display = ''
        # if 'show_display' in request.GET.keys():
        #     show_display = request.GET.get('show_display')
        # s = str(apps.CAR_ID).rjust(4, '0')
        # s = f'car{s}:{self.display}'
        params = {
            'cad_id': 1,            # apps.CAR_ID,
            'display_id': '/e21',    # s,
            'show_display': 'd-none'      # show_display
        }
        return render(request, self.template_name, params)
