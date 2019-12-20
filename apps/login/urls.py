# -*- coding: utf-8 -*-
from django.urls import path

from .views import UserFormView

app_name = 'login'
urlpatterns = [
    path('login', UserFormView.as_view(), name='login'),
]
