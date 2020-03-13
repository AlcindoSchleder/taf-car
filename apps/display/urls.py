# -*- coding: utf-8 -*-
from django.urls import path

from .views import DisplayPageView

app_name = 'display'
urlpatterns = [
    path('', DisplayPageView.as_view(), name='display'),
    path('<str:display_id>', DisplayPageView.as_view(), name='display'),
]
