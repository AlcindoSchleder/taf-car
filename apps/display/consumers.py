# -*- coding: utf-8 -*-
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class DisplayConsumer(AsyncWebsocketConsumer):
    display_id = ''
    car_id = ''
    group_id = ''
    channel_name = ''

    async def connect(self):
        self.display_id = self.scope['url_route']['kwargs']['display_id']
        self.car_id = self.scope['url_route']['kwargs']['car_id']
        self.group_id = f'display_{self.car_id}'
        self.channel_name = f'display_{self.car_id}_{self.display_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.group_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        car_id = text_data_json['car_id']
        display_id = text_data_json['display']
        message = text_data_json['message']

        # Send message to display if display_id = none send to group 'car_id'
        await self.channel_layer.group_send(
            self.group_id,
            {
                'type': 'json_message',
                'command': command,
                'car_id': car_id,
                'display_id': display_id,
                'message': message,
            }
        )

    # Receive message from room group
    async def json_message(self, event):
        command = event['command']
        car_id = event['car_id']
        display_id = event['display_id']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'command': command,
            'car_id': car_id,
            'display_id': display_id,
            'message': message,
        }))
