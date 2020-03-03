# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import CarriersCars, Products, CarriersProducts

# Register your models here.
admin.site.register(Products)
admin.site.register(CarriersCars)
admin.site.register(CarriersProducts)
