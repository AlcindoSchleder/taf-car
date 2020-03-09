# -*- coding: utf-8 -*-
from django.urls import path

from .views import HomePageView, HomeTestsView

app_name = 'home'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('tests/', HomeTestsView.as_view(), name='tests'),
]
