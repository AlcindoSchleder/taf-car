# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import json
import apps
from rest_framework import viewsets
from rest_framework.response import Response
from decouple import config
from apis.mqtt.mqtt import MqttManager
from apps.home.models import CarBoxesMessage


class MqttViewSet(viewsets.ViewSet):
    """
    API endpoint that allows send messages from mqtt server.
    """
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    MQTT_HOST = config('MQTT_HOST', default='192.168.0.20')
    MQTT_PORT = int(config('MQTT_PORT', default=1883))
    MQTT_CLIENT_ID = config('MQTT_CLIENT_ID', default='iCity_car_v1.0')
    MQTT_USER = config('MQTT_USER')
    MQTT_PASSWORD = config('MQTT_PASSWORD')
    MQTT_TOPIC_BASE = '/taf/car'

    service = None
    mqtt_payload = ''
    result = apps.RESULT_DICT

    def _config_service_manager(self, carid:int):
        apps.CAR_ID = carid
        if carid > 0:
            s = str(carid).rjust(4, '0')
            self.MQTT_TOPIC_BASE = f'/taf/car{s}'

        self.service = MqttManager(
            self.MQTT_HOST,
            self.MQTT_PORT,
            self.MQTT_TOPIC_BASE,
            self.MQTT_USER,
            self.MQTT_PASSWORD
        )

    def _config_message(self, command_type, carid, display, message) -> dict:
        self.mqtt_payload = {
            "type": command_type,
            "carid": int(carid),
            "display": display,
            "message": message,
        }
        self._config_service_manager(self.mqtt_payload['carid'])
        return self.mqtt_payload

    def send_message(self, request, *args, **kwargs):
        """
        Send a message to Mqtt Server
        """
        self._config_message(
            request.query_params.get('type'),
            request.query_params.get('carid'),
            request.query_params.get('display'),
            request.query_params.get('message')
        )
        try:
            self.service.connect()
            self.service.publish(self.mqtt_payload, self.mqtt_payload['display'])
        except Exception as e:
            self.result['status']['sttCode'] = 500
            self.result['status']['sttMsgs'] = f'Error: Not send a message! - Error: {e}'
            return Response(self.result, 500)
        finally:
            if self.service.is_connected:
                self.service.disconnect()
        self.result['status']['sttMsgs'] = 'Mensagem publicada com sucesso!'
        self.result['publish'] = {
            'payload': self.mqtt_payload,
            'topic': f'{self.MQTT_TOPIC_BASE}/{self.mqtt_payload["display"]}'
        }
        return Response(self.result, 200)

    def send_command(self, request, *args, **kwargs):
        """
        Send a message to Mqtt Server
        """
        self._config_message(
            request.query_params.get('type'),
            request.query_params.get('carid'),
            request.query_params.get('display'),
            request.query_params.get('message')
        )
        try:
            self.service.connect()
            self.service.publish(self.mqtt_payload, self.mqtt_payload['display'])
        except Exception as e:
            self.result['status']['sttCode'] = 500
            self.result['status']['sttMsgs'] = f'Error: Not send a message! - Error: {e}'
            return Response(self.result, 500)
        finally:
            if self.service.is_connected:
                self.service.disconnect()
        self.result['status']['sttMsgs'] = 'Mensagem publicada com sucesso!'
        self.result['publish'] = {
            'payload': self.mqtt_payload,
            'topic': f'{self.MQTT_TOPIC_BASE}/{self.mqtt_payload["display"]}'
        }
        return Response(self.result, 200)

    def check_changes(self, request, *args, **kwargs):
        """
        check Changes to display boxes stored on databses
        """
        car_id = request.query_params.get('car_id'),
        display_id = request.query_params.get('display_id'),
        date_hour = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        msgs = CarBoxesMessage.objects.filter(
            fk_cars=car_id,
            fk_car_boxes=display_id,
            capture_date__gt=date_hour,
            flag_captured=0
        ).all()
        return Response(dict(msgs), 200)
