# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UsersOperation(models.Model):
    FLAG_USER_CHOICHES = [
        (0, "Usuário do Sistema"),
        (1, "Gerente de Departamento"),
        (2, "Supervisor do Departamento"),
        (3, "Conferente"),
        (4, "Coletor de Mercadorias"),
    ]
    fk_users = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    flag_tuser = models.SmallIntegerField(choices=FLAG_USER_CHOICHES, verbose_name='Código')
    biometric_id = models.BinaryField(verbose_name='Biometria')
