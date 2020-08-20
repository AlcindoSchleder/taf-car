# -*- coding: utf-8 -*-
from django.urls import path

from .views import HomePageView, HomeTestsView, OperationPageView

app_name = 'home'
urlpatterns = [
    path('<int:car_id>', HomePageView.as_view(), name='home'),
    path('operation/<int:car_id>', OperationPageView.as_view(), name='home'),
    path('tests/<str:type>/<int:car_id>', HomeTestsView.as_view(), name='tests'),
]
