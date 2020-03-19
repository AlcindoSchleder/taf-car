# -*- coding: utf-8 -*-
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/display/<car_id>/', consumers.DisplayConsumer),
    path('ws/display/<car_id>/<display_id>/', consumers.DisplayConsumer),
]
