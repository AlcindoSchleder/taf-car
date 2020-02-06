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
        verbose_name_plural = 'Cars'

    def __str__(self):
        return self.dsc_car


class CarsBoxes(models.Model):
    pk_carboxes = models.AutoField(primary_key=True, verbose_name='ID')
    box_name = models.CharField(max_length=30, verbose_name='Código do Box')
    fk_cars = models.ForeignKey(Cars, on_delete=models.CASCADE, verbose_name='Carro')
    fisical_box_id = models.CharField(max_length=20, verbose_name='Código da Caçamba')

    class Meta:
        db_table = 'cars_boxes'
        verbose_name_plural = 'CarsBoxes'

    def clear_box_id(self, car: int = 0):
        if car == 0:
            return
        self.fisical_box_id = ''
        return

    def __str__(self):
        return self.fk_cars.dsc_car + ' - box:' + self.box_name
