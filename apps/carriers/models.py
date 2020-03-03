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
    pk_carriers_products = models.IntegerField(primary_key=True, default=0, verbose_name='Código')
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
    status = models.CharField(max_length=1, null=True, blank=True, verbose_name='Status')
    insert_date = models.DateTimeField(auto_now=True, verbose_name='Data')

    class Meta:
        db_table = 'cargo_products'


class LastCharge(models.Model):
    pk_last_charge = models.SmallIntegerField(primary_key=True, verbose_name='Código da Carga', default=1)
    date_last_charge = models.DateTimeField(auto_now=True, verbose_name='Data da Carga')

    class Meta:
        db_table = 'app_last_charge'


class Products(models.Model):
    pk_products = models.IntegerField(primary_key=True, verbose_name='Código')
    dsc_prod = models.CharField(max_length=50, verbose_name='Descrição')
    volume = models.FloatField(verbose_name='Volume')
    weight = models.FloatField(verbose_name='Peso')
    unity = models.CharField(max_length=5, verbose_name='Unidade')
    qtd_unity = models.FloatField(verbose_name='QUant. da Unidade')
    image_prod = models.TextField(blank=True, null=True, verbose_name='Imagem')     # Base64 decoded image (text)


class CarriersCars(models.Model):
    """
    Table that store all collects to do on 1 car
    """
    SIDE_OPTIONS = [
        ('E', 'Esquerda'),
        ('D', 'Direita'),
    ]
    # hash contendo o usuário, o carro, a carga, o pedido, e o box
    pk_carriers_cars = models.CharField(max_length=64, primary_key=True, verbose_name='Usuario/Carga')
    fk_cars = models.ForeignKey(Cars, on_delete=models.PROTECT, verbose_name='Carro')
    fk_cars_boxes = models.ForeignKey(CarsBoxes, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Box')
    fk_customer = models.IntegerField(blank=True, default=0, verbose_name='Cod. Cliente')
    fk_products = models.ForeignKey(CarriersProducts, on_delete=models.PROTECT, verbose_name='Produto')
    charge = models.IntegerField(verbose_name='Num. Carga')
    lot = models.IntegerField(verbose_name='Num Lote')
    street = models.CharField(max_length=3, verbose_name='Rua')
    tower = models.CharField(max_length=5, verbose_name='Predio')
    level = models.CharField(max_length=3, verbose_name='Nivel')
    position = models.CharField(max_length=5, verbose_name='Posicao')
    stock = models.FloatField(verbose_name='Estoque Atual')
    qtd_packing = models.FloatField(verbose_name='Quant. da Embalagem')
    qtd_order = models.FloatField(verbose_name='Quant. do Pedido')
    qtd_collected = models.FloatField(verbose_name='Quant. Coletada')
    unity = models.CharField(max_length=2, verbose_name='UN')
    weight = models.FloatField(verbose_name='Peso')
    volume = models.FloatField(verbose_name='Volume m3')
    weight_box = models.FloatField(verbose_name='Peso do Box')
    volume_box = models.FloatField(verbose_name='Volume do Box')
    side = models.CharField(
        max_length=1,
        choices=SIDE_OPTIONS,
        default='E',
        verbose_name='Lado'
    )
    flag_status = models.SmallIntegerField(default=0, verbose_name='Status')
    flag_ready = models.SmallIntegerField(default=0, verbose_name='Carregado')
    flag_conference = models.SmallIntegerField(default=0, verbose_name='Conferido')
    insert_date = models.DateTimeField(auto_now=True, verbose_name='Data de Insercao')

    class Meta:
        db_table = 'carrier_products'
