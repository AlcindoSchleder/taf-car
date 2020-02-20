# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from decouple import config
from apis.mqtt.mqtt import MqttManager
from apps import CAR_ID, RESULT_DICT


class MqttViewSet(viewsets.ViewSet):
    """
    API endpoint that allows send messages from mqtt server.
    """
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    MQTT_HOST = config('MQTT_HOST', default='192.168.0.203')
    MQTT_PORT = int(config('MQTT_PORT', default=1883))
    MQTT_CLIENT_ID = config('MQTT_CLIENT_ID', default='iCity_car_v1.0')
    MQTT_USER = config('MQTT_USER')
    MQTT_PASSWORD = config('MQTT_PASSWORD')
    TOPIC_CAR = str(CAR_ID).rjust(4, '0')
    MQTT_TOPIC_BASE = f'/taf/car{TOPIC_CAR}'

    service = MqttManager(MQTT_HOST, MQTT_PORT, MQTT_TOPIC_BASE, MQTT_USER, MQTT_PASSWORD)
    mqtt_payload = ''
    result = RESULT_DICT

    def send_message(self, request, *args, **kwargs):
        """
        Send a message to Mqtt Server
        """
        try:
            self.service.connect()
            payload = kwargs.get('payload')
            end_topic = kwargs.get('end_topic')
            self.service.publish(payload, end_topic)
        except Exception as e:
            self.result['status']['sttCode'] = 500
            self.result['status']['sttMsgs'] = f'Error: Not send a message! - Error: {e}'
            return Response(self.result, 500)
        finally:
            if self.service.is_connected:
                self.service.disconnect()
        self.result['status']['sttMsgs'] = 'Mensagem publicada com sucesso!'
        self.result['publish'] = {'payload': payload, 'topic': f'{self.MQTT_TOPIC_BASE}/{end_topic}'}
        return Response(self.result, 200)
