# -*- coding: utf-8 -*-
from django.urls import path
from .consumers import DisplayConsumer

display_urlpatterns = [
    path('ws/car/<car_id>/', DisplayConsumer),
    path('ws/display/<car_id>/<display_id>/', DisplayConsumer),
]
