# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import apps
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from apps.home.models import Cars, CarsBoxes, CarBoxesMessage


class MqttViewSet(viewsets.ViewSet):
    """
    API endpoint that allows send messages from mqtt server.
    """
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    result = apps.RESULT_DICT

    def publish_message_into_db(self, command_type, car_id, display, message):
        """
        Save a message into database
        """
        self.result = apps.RESULT_DICT
        apps.CAR_ID = car_id
        try:
            car = Cars.objects.get(pk=car_id)
            carboxes = CarsBoxes.objects.get(pk=int(display.replace('e', '')))
            display_message = CarBoxesMessage()
            display_message.fk_car_boxes = carboxes
            display_message.flag_captured = 0
            display_message.box_type_command = command_type
            display_message.box_name = display
            display_message.fk_cars = car
            display_message.box_message = message
            display_message.capture_date = datetime.now(tz=timezone.utc)
            display_message.save()
            self.result['status']['sttMsgs'] = f'Mensagem publicada com sucesso! - ({message})'
        except Exception as e:
            self.result['status']['sttCode'] = 500
            self.result['status']['sttMsgs'] = f'Erro ao gravar a mensagem no database. ({e})'

    def send_message(self, request, *args, **kwargs):
        """
        Send a message to display
        """
        self.result = apps.RESULT_DICT
        self.publish_message_into_db(
            request.query_params.get('type'),
            request.query_params.get('car_id'),
            request.query_params.get('display'),
            request.query_params.get('message')
        )
        return Response(self.result, self.result['status']['sttCode'])

    def _get_message_dictionary(self, data):
        return {
            'fk_car_boxes': data.fk_car_boxes.pk,
            'flag_captured': data.flag_captured,
            'box_type_command': data.box_type_command,
            'box_name': data.box_name,
            'fk_cars': data.fk_cars.pk,
            'box_message': data.box_message,
            'capture_date': data.capture_date,
            'update_date': data.update_date,
            'insert_date': data.insert_date
        }

    def check_changes(self, request, *args, **kwargs):
        """
        check Changes to display boxes stored on databses
        """
        self.result = apps.result_dict()
        car_id = request.query_params.get('car_id')
        display_id = request.query_params.get('display_id')
        fk_display = display_id.replace('e', '')
        # date_hour = datetime.now(tz=timezone.utc) - timedelta(hours=0, minutes=1, seconds=0)
        try:
            for msg in CarBoxesMessage.objects.filter(
                fk_cars=car_id,
                fk_car_boxes=int(fk_display),
                flag_captured=0
            ):
                self.result['data'].append(self._get_message_dictionary(msg))

                msg.flag_captured = 1
                msg.captured_date = datetime.now(tz=timezone.utc)
                msg.save()
        except Exception as e:
            self.result['status']['sttCode'] = 500
            self.result['status']['sttMsgs'] = f'Erro ao buscar as mensagens: {e}'
        # HOw to return this message?
        return Response(self.result, self.result['status']['sttCode'])
