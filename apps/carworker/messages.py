# -*- coding: utf-8 -*-
import json
from channels.layers import get_channel_layer


class AsyncMessages:

    @staticmethod
    async def send_message_to_member(command: str, car_id: int, member: str, message: str):
        channel_layer = get_channel_layer()
        message = {
            'type': 'json.message',
            'command': command,
            'car_id': car_id,
            'display_id': member,
            'message': message,
        }
        group_id = f'display_{car_id}_{member}'
        await channel_layer.send(group_id, text_data=json.dumps({
            'message': message
        }))

    @staticmethod
    async def send_message_to_group(command: str, car_id: int, message: str):
        channel_layer = get_channel_layer()
        message = {
            'type': 'json.message',
            'command': command,
            'car_id': car_id,
            'message': message,
        }
        group_id = f'display_{car_id}'
        await channel_layer.group_send(group_id, text_data=json.dumps({
            'message': message
        }))
