# -*- coding: utf-8 -*-
from django.urls import path

from .views import DisplayPageView

app_name = 'display'
urlpatterns = [
    path('<int:car_id>/<str:display_id>/', DisplayPageView.as_view(), name='display'),
]
