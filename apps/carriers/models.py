# -*- coding: utf-8 -*-
from django.db import models
from apps.home.models import Cars, CarsBoxes


class CarriersProducts(models.Model):
    FLAG_TYPE_ADDRESS = [
        ('A', 'Grandeza'),
        ('M', 'Miudeza'),
    ]
    FLAG_TYPE_LOCAL = [
        ('T', 'Térreo'),
        ('A', 'Aéreo'),
    ]
    FLAG_STATUS_ADDRESS = [
        ('D', 'Disponível'),
        ('O', 'Ocupado'),
        ('B', 'Bloqueado'),
        ('R', 'Reservado'),
        ('I', 'Inativo'),
        ('E', 'Restrito'),
        ('Q', 'Quarentena'),
    ]
    FLAG_STATUS_CARGO = [
        ('A', 'Aguardando'),
        ('F', 'Faturada'),
        ('G', 'Gerada'),
        ('L', 'Liberada'),
        ('S', 'Em Separação'),
        ('T', 'Termo de Liberação'),
        ('C', 'Gerando Carregamento'),
        ('X', 'Iniciado Processo de Cancelamento da Carga'),
    ]
    FLAG_STATUS_ACTIVITY = [
        ('A', 'Aguardando'),
        ('E', 'Em Execução'),
        ('X', 'Cancelada'),
        ('F', 'Finalizada'),

    ]
    pk_products = models.AutoField(primary_key=True, verbose_name='Código')
    nroempresa = models.IntegerField(verbose_name='Empresa')
    nrocarga = models.IntegerField(verbose_name='Carga')
    seqlote = models.IntegerField(verbose_name='Lote')
    seqtarefa = models.IntegerField(null=True, blank=True, verbose_name='Tarefa')
    seqatividade = models.IntegerField(verbose_name='Aitividade')
    seqproduto = models.IntegerField(verbose_name='Produto')
    desccompleta = models.CharField(max_length=100, verbose_name='Descrição')
    descreduzida = models.CharField(max_length=50, verbose_name='Descrição')
    codrua = models.CharField(max_length=3, verbose_name='Rua')
    nropredio = models.SmallIntegerField(verbose_name='Prédio')
    nroapartamento = models.SmallIntegerField(verbose_name='Nível')
    nrosala = models.SmallIntegerField(verbose_name='Local')
    especieendereco = models.CharField(max_length=1, choices=FLAG_TYPE_ADDRESS, verbose_name='Tipo End.')
    indterreoaereo = models.CharField(max_length=1, choices=FLAG_TYPE_LOCAL, verbose_name='Tipo Local')
    qtdembalagem = models.FloatField(verbose_name='Qtd. Embalagem')
    qtdatual = models.FloatField(verbose_name='Qtd. Atual')
    statusendereco = models.CharField(max_length=1, choices=FLAG_STATUS_ADDRESS, verbose_name='Tipo Local')
    tipespecie = models.CharField(max_length=1, null=True, blank=True, verbose_name='Tipo Espécie')
    coddepossepar = models.SmallIntegerField(verbose_name='Depós. Separ.')
    destino = models.CharField(max_length=40, verbose_name='Destino')
    tipentrega = models.CharField(max_length=1, null=True, blank=True, verbose_name='Tipo Entrega')
    mcubtotal = models.FloatField(verbose_name='Cubagem')
    pesototal = models.FloatField(verbose_name='Peso')
    nrobox = models.SmallIntegerField(verbose_name='Box do Lote')
    statuscarga = models.CharField(max_length=1, choices=FLAG_STATUS_CARGO, verbose_name='Status da Carga')
    valorcarga = models.FloatField(verbose_name='Valor da Carga')
    qtdembcargasep = models.FloatField(verbose_name='Qtd. Emb. Separ.')
    qtdcontada = models.FloatField(verbose_name='Qtd. Emb. Contada')
    qtdembsolcargasep = models.FloatField(verbose_name='Qtd. Emb. Carga Solic.')
    qtdembsepcargasep = models.FloatField(verbose_name='Qtd. Emb. Carga Separ.')
    codtipatividade = models.CharField(max_length=2, verbose_name='Código Atividade')
    nroquebra = models.SmallIntegerField(verbose_name='Quebra')
    mesano = models.CharField(null=True, blank=True, max_length=5, verbose_name='Mês/Ano')
    peso = models.FloatField(verbose_name='Peso.')
    metragemcubica = models.FloatField(verbose_name='Cubagem')
    qtdvolume = models.FloatField(verbose_name='Volumnes')
    qtditem = models.FloatField(verbose_name='Items')
    indexclusao = models.CharField(max_length=1, verbose_name='Excluído')
    grauprioridade = models.IntegerField(verbose_name='Prioridade')
    statusrf = models.CharField(max_length=1, null=True, blank=True, verbose_name='Status RF')
    statusatividade = models.CharField(max_length=1, choices=FLAG_STATUS_ACTIVITY, verbose_name='Status da Atividade')
    tipseparacao = models.CharField(max_length=2, null=True, blank=True, verbose_name='Tipo Serpação')
    tiplote = models.CharField(max_length=2, null=True, blank=True, verbose_name='Tipo Lote')
    pesototallote = models.FloatField(verbose_name='Peso Lote')
    mcubtotallote = models.FloatField(verbose_name='Cubagem Lote')
    qtdvolumelote = models.FloatField(verbose_name='Valumes Lote')
    qtditemlote = models.FloatField(verbose_name='Items do Lote')
    seqordenacaoseparacao = models.IntegerField(verbose_name='Ordem Separação')
    seqpessoa = models.IntegerField(verbose_name='Código Cliente')
    qtdembsolcarga = models.FloatField(verbose_name='Qtd. Emb. Solic.')
    qtdembcarga = models.FloatField(verbose_name='Qtd. Emb.')
    qtdembsepcarga = models.FloatField(verbose_name='Qtd. Emb. Separada')
    nropedvenda = models.IntegerField(null=True, blank=True, verbose_name='Número Pedido')
    insert_date = models.DateTimeField(auto_now=True, verbose_name='Data')

    class Meta:
        db_table = 'cargo_products'


class CarriersProductsCars(models.Model):
    # this field is a hash of the box id, barcode, order_number and customer order id
    pk_products_cars = models.CharField(max_length=64, primary_key=True, verbose_name='Box')
    fk_carriers_products = models.ForeignKey(CarriersProducts, on_delete=models.CASCADE, verbose_name='Produto')
    fk_cars = models.ForeignKey(Cars, on_delete=models.PROTECT, verbose_name='Carro')
    fk_cars_boxes = models.ForeignKey(CarsBoxes, on_delete=models.PROTECT, verbose_name='Box')
    insert_date = models.DateTimeField(auto_now=True, verbose_name='Data')

    class Meta:
        db_table = 'carriers_products_cars'
