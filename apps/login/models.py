# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from apps.home.models import Cars


class UsersOperators(models.Model):
    FLAG_USER_CHOICHES = [
        (0, "Usuário do Sistema"),
        (1, "Gerente de Departamento"),
        (2, "Supervisor do Departamento"),
        (3, "Conferente"),
        (4, "Produtivo"),
    ]
    FLAG_FUNCTION_TYPE = [
        ('S', 'Separador'),
        ('M', 'Movimentador'),
        ('C', 'Conferente'),
    ]
    FLAG_STATUS_OPERATOR = [
        ('I', 'Inativo'),
        ('A', 'Ativo'),
    ]
    FLAG_TRUE_FALSE = [
        ('S', 'Sim'),
        ('N', 'Não'),
    ]
    fk_users = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name='Código')
    user_integration = models.IntegerField(default=1, verbose_name='Código')
    flag_tuser = models.SmallIntegerField(choices=FLAG_USER_CHOICHES, verbose_name='Tipo')
    biometric_id = models.BinaryField(null=True, blank=True, verbose_name='Biometria')
    nroempresa = models.IntegerField(verbose_name='Empresa')
    tipprodutivo = models.CharField(
        max_length=1, choices=FLAG_STATUS_OPERATOR, default='S', verbose_name='Status'
    )
    statusprodutivo = models.CharField(
        max_length=1, choices=FLAG_FUNCTION_TYPE, default='S', verbose_name='Tipo Função'
    )
    inddisponibilidade = models.CharField(
        max_length=1, choices=FLAG_TRUE_FALSE, default='S', verbose_name='Disponível'
    )
    horinijornada = models.TimeField(verbose_name='Hora início')
    horfimjornada = models.TimeField(verbose_name='Hora Fim')
    fk_cars = models.ForeignKey(Cars, on_delete=models.PROTECT, verbose_name='Carro Alocado')
    insert_date = models.DateTimeField(auto_now_add=True, verbose_name='Data e Hora da Inserção')

    class Meta:
        db_table = 'user_operators'


class UsersOperatorsPermissions(models.Model):
    TYPE_LINE_OPTIONS = [
        ('AG', 'Alimetício Grandeza'),
        ('BF', 'Fardarias Grandeza'),
        ('BG', 'Bebidas Grandeza'),
        ('CO', 'Confinado'),
        ('FA', 'Fracionado Alimento'),
        ('FB', 'Fracionado Bebidas'),
        ('FF', 'Leveza Papel Higiênico'),
        ('FG', 'Fracionado Gerais'),
        ('FL', 'Leveza Fardaria Randeza'),
        ('LA', 'Licitação Alimento'),
        ('LF', 'Limpeza Fracionada'),
        ('LG', 'Limpeza Grandeza'),
        ('LL', 'Leveza Limpeza Grandeza'),
    ]
    FLAG_STATUS = [
        ('A', 'Ativa'),
        ('I', 'Inativa'),
    ]
    #
    # Primary key contains user_name and number of permission
    #
    pk_user_permissions = models.CharField(max_length=30, primary_key=True, verbose_name='User-Permisson')
    fk_users = models.ForeignKey(User, default=0, on_delete=models.CASCADE, verbose_name='Usuário')
    type_line = models.CharField(max_length=2, default='Lf', choices=TYPE_LINE_OPTIONS, verbose_name='Linha de Separação')
    dsc_line = models.CharField(max_length=50, verbose_name='Descrição')
    flag_separation = models.CharField(max_length=1, default='R', verbose_name='Separação')
    flag_status = models.CharField(max_length=1, default='A', choices=FLAG_STATUS, verbose_name='status')

    class Meta:
        db_table = 'user_permissions'

    def __str__(self):
        return f'{self.desclinhasepar} - {self.codlinhasepar}'
