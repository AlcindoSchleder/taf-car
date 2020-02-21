# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Cars, CarsBoxes, CarBoxesMessage

# Register your models here.
admin.site.register(Cars)
admin.site.register(CarsBoxes)
admin.site.register(CarBoxesMessage)
