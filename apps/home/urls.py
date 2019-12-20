# -*- coding: utf-8 -*-
from django.urls import path

from .views import HomePageView, UserFormView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login', UserFormView.as_view(), name='login')
]
