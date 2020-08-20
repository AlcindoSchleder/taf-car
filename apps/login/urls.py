# -*- coding: utf-8 -*-
from django.urls import path

from .views import UserFormView, CollectorRegisterView

app_name = 'login'
urlpatterns = [
    path('', UserFormView.as_view(), name='login'),
    path('signup/', CollectorRegisterView.as_view(), name='signup'),
]
