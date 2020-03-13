# -*- coding: utf-8 -*-
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/display/(?P<display_id>\w+)/$', consumers.ChatConsumer),
]
