# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    CargasProdutos, LastCharge, Products, ProductsSimilar, Carriers, CarriersProducts, CarriersBoxes
)

# Register your models here.


class CargasProdutosAdmin(admin.ModelAdmin):
    list_display = (
        'nrocarga', 'seqlote', 'seqpessoa', 'desccompleta', 'tipseparacao',
        'codrua', 'nropredio', 'embalagem', 'pesobruto', 'pesoliquido',
        'altura', 'largura', 'profundidade', 'status'
    )


class LastChargeAdmin(admin.ModelAdmin):
    list_display = ('pk_last_charge', 'fk_customer', 'fk_product', 'date_last_charge')


class CarriersAdmin(admin.ModelAdmin):
    list_display = (
        'charge', 'lot', 'fk_customer', 'weight_charge', 'volume_charge'
    )


# class CarriersProductsAdmin(admin.ModelAdmin):
#     list_display = (
#         'fk_products', 'street', 'tower', 'qtd_order', 'unity',
#         'stock', 'weight', 'volume', 'side', 'status',
#     )


admin.site.register(CargasProdutos, CargasProdutosAdmin)
admin.site.register(LastCharge, LastChargeAdmin)
admin.site.register(Carriers, CarriersAdmin)
# admin.site.register(CarriersProducts, CarriersProductsAdmin)
admin.site.register(Products)
