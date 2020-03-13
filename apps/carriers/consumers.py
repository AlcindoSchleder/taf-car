# -*- coding: utf-8 -*-
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class CarriersConsumer(AsyncWebsocketConsumer):
    display_id = ''
    car_id = ''

    async def connect(self):
        self.display_id = self.scope['url_route']['kwargs']['display_id']
        self.car_id = 'display_%s' % self.display_id

        # Join room group
        await self.channel_layer.group_add(
            self.car_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.car_id,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.car_id,
            {
                'type': 'control',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
