# -*- coding: utf-8 -*-
from django.urls import path
from .views import CarriersPageView

app_name = 'carriers'
urlpatterns = [
    path('carriers', CarriersPageView.as_view(), name='carriers'),
]
