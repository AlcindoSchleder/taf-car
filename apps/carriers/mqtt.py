# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from apps import RESULT_DICT, CAR_ID


class MqttManager:
    result = RESULT_DICT
    server = ''
    port = 0
    client = mqtt.Client()
    topic = ''
    is_connected = False

    def __init__(self, server: str = '192.168.0.203', port=1883, topic=f'taf/car{CAR_ID}/#'):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.server = server
        self.port = port
        self.topic = topic

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe(self.topic)

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
            print(f"Client can't Connected on MQTT Server: {self.server}:{self.port} error: {e}")

    def disconnect(self):
        if self.client.is_connected():
            self.is_connected = False
            self.client.loop_stop()
            self.client.disconnect()

    def client_loop(self):
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_start()
