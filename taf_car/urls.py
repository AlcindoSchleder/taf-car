# -*- coding: utf-8 -*-
"""
    taf_car URL Configuration
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls')),
    path('login/', include('apps.login.urls')),
    path('carriers/', include('apps.carriers.urls')),
]
