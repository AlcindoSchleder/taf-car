# -*- coding: utf-8 -*-
"""
    taf_car URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apis.mqtt.api.viewsets import MqttViewSet

router = routers.DefaultRouter()
router.register(r'mqtt', MqttViewSet, basename='mqtt')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls', 'home')),
    path('login/', include('apps.login.urls', 'login')),
    path('carriers/', include('apps.carriers.urls', 'carriers')),
    path('display/', include('apps.display.urls', 'display')),
    path(
        'api/mqtt/send_message/',
        MqttViewSet.as_view(actions={"get": "send_message"}),
        name='api_send_message'
    ),
    path(
        'api/mqtt/check_changes/',
        MqttViewSet.as_view(actions={"get": "check_changes"}),
        name='api_check_changes'
    ),
    path('api/', include(router.urls))
]
