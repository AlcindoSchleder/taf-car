# -*- coding: utf-8 -*-
from django.db import models


class Cars(models.Model):
    pk_cars = models.AutoField(primary_key=True, verbose_name='Código do Carro')
    dsc_car = models.CharField(max_length=50, verbose_name='Descrição')
    factory_serial = models.CharField(max_length=64, verbose_name='Núm. Serial')
    date_factory = models.DateTimeField(verbose_name='Data Fabr.')
    date_insert = models.DateTimeField(auto_now=True, verbose_name='Data Inserção')

    class Meta:
        db_table = 'cars'


class CarsBoxes(models.Model):
    pk_carboxes = models.IntegerField(primary_key=True, verbose_name='Código do Box')
    fk_cars = models.ForeignKey(Cars, on_delete=models.CASCADE, verbose_name='Carro')
    box_name = models.CharField(max_length=30, verbose_name='Nome do Box')

    class Meta:
        db_table = 'cars_boxes'
