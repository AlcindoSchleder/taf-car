# -*- coding: utf-8 -*-
"""
    taf_car URL Configuration
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls', 'home')),
    path('login/', include('apps.login.urls', 'login')),
    path('carriers/', include('apps.carriers.urls', 'carriers')),
    path('display/', include('apps.display.urls', 'display')),
]
