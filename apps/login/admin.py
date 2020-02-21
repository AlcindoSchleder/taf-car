# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import UsersOperatorsPermissions, UsersOperators

# Register your models here.
admin.site.register(UsersOperatorsPermissions)
admin.site.register(UsersOperators)