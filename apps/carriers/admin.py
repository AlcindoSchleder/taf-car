# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import UserProducts, LastProductCharge, CarriersProducts

# Register your models here.
admin.site.register(UserProducts)
admin.site.register(LastProductCharge)
admin.site.register(CarriersProducts)
