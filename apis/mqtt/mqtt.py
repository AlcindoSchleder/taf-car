# -*- coding: utf-8 -*-
import json
from datetime import datetime
from random import randint
import paho.mqtt.client as mqtt
from apps import RESULT_DICT, CAR_ID


class MqttManager:
    result = RESULT_DICT
    server = ''
    port = 0
    prefix = 'iCity'
    time = datetime.now().strftime("%H:%M:%S")
    rnd_id = randint(0, 1000000)
    client = mqtt.Client(f'{prefix}:{time}-{rnd_id}')
    topic = ''
    is_connected = False

    def __init__(self, server: str = '192.168.0.203', port=1883, topic='/iCity/mqtt', user=None, password=None):
        if user is not None and password is not None:
            self.client.username_pw_set(username=user, password=password)
        self.topic = topic
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.server = server
        self.port = port

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        pass
        # print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # self.client.subscribe(self.topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        if self.is_connected:
            print(msg.topic + " " + str(msg.payload))

    # The callback for when client receives a disconnect() response from server
    def on_disconnect(self):
        if self.is_connected:
            self.client.reconnect()

    def connect(self):
        try:
            self.client.connect(self.server, self.port, 60)
            self.is_connected = True
        except Exception as e:
            raise Exception(f'Client can not Connected on MQTT Server: {self.server}:{self.port} error: {e}')

    def disconnect(self):
        if self.client.is_connected():
            self.is_connected = False
            self.client_loop()
            self.client.disconnect()

    def client_loop(self):
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        if self.is_connected:
            self.client.loop_start()
        else:
            self.client.loop_stop()

    def publish(self, payload, end_topic: str):
        payload = json.dumps(payload) if type(payload) == 'dict' else str(payload)
        topic = self.topic if end_topic == '' else f'{self.topic}/{end_topic}'
        self.client.publish(topic, payload)

    def subscribe(self, end_topic: str):
        topic = self.topic if end_topic == '' else f'{self.topic}/{end_topic}'
        self.client.subscribe(topic)
        self.client_loop()
