# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from apps.home.models import Cars, CarsBoxes
from django.contrib.auth.models import User


class CargasProdutos(models.Model):
    TYPE_LINE_OPTIONS = [
        ('AG', 'Alimetício Grandeza'),
        ('BF', 'Fardarias Grandeza'),
        ('BG', 'Bebidas Grandeza'),
        ('CO', 'Confinado'),
        ('FA', 'Fracionado Alimento'),
        ('FB', 'Fracionado Bebidas'),
        ('FF', 'Leveza Papel Higiênico'),
        ('FR', 'Fracionado Alimento'),
        ('FG', 'Fracionado Gerais'),
        ('FL', 'Leveza Fardaria Grandeza'),
        ('LA', 'Licitação Alimento'),
        ('LF', 'Limpeza Fracionada'),
        ('LG', 'Limpeza Grandeza'),
        ('LL', 'Leveza Limpeza Grandeza'),
    ]
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
    pk_cargas_produtos = models.AutoField(primary_key=True, verbose_name='Código de Acesso')
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
    qtdembalagem = models.FloatField(default=0.00, verbose_name='Qtd. Embalagem')
    qtdatual = models.FloatField(default=0.00, verbose_name='Qtd. Atual')
    statusendereco = models.CharField(max_length=1, choices=FLAG_STATUS_ADDRESS, verbose_name='Tipo Local')
    tipespecie = models.CharField(max_length=1, null=True, blank=True, verbose_name='Tipo Espécie')
    coddepossepar = models.SmallIntegerField(verbose_name='Depós. Separ.')
    destino = models.CharField(max_length=40, verbose_name='Destino')
    tipentrega = models.CharField(max_length=1, null=True, blank=True, verbose_name='Tipo Entrega')
    mcubtotal = models.FloatField(default=0.00, verbose_name='Cubagem')
    pesototal = models.FloatField(default=0.00, verbose_name='Peso')
    nrobox = models.SmallIntegerField(verbose_name='Box do Lote')
    statuscarga = models.CharField(max_length=1, choices=FLAG_STATUS_CARGO, verbose_name='Status da Carga')
    valorcarga = models.FloatField(default=0.00, verbose_name='Valor da Carga')
    qtdembcargasep = models.FloatField(default=0.00, verbose_name='Qtd. Emb. Separ.')
    qtdcontada = models.FloatField(default=0.00, verbose_name='Qtd. Emb. Contada')
    qtdembsolcargasep = models.FloatField(default=0.00, verbose_name='Qtd. Emb. Carga Solic.')
    qtdembsepcargasep = models.FloatField(default=0.00, verbose_name='Qtd. Emb. Carga Separ.')
    codtipatividade = models.CharField(max_length=2, verbose_name='Código Atividade')
    nroquebra = models.SmallIntegerField(verbose_name='Quebra')
    mesano = models.CharField(null=True, blank=True, max_length=5, verbose_name='Mês/Ano')
    metragemcubica = models.FloatField(default=0.00, verbose_name='Cubagem')
    qtdvolume = models.FloatField(default=0.00, verbose_name='Volumnes')
    qtditem = models.FloatField(default=0.00, verbose_name='Items')
    indexclusao = models.CharField(max_length=1, verbose_name='Excluído')
    grauprioridade = models.IntegerField(verbose_name='Prioridade')
    statusrf = models.CharField(max_length=1, null=True, blank=True, verbose_name='Status RF')
    statusatividade = models.CharField(max_length=1, choices=FLAG_STATUS_ACTIVITY, verbose_name='Status da Atividade')
    tipseparacao = models.CharField(
        max_length=2, null=True, blank=True, choices=TYPE_LINE_OPTIONS, verbose_name='Tipo Serpação'
    )
    tiplote = models.CharField(max_length=2, null=True, blank=True, verbose_name='Tipo Lote')
    pesototallote = models.FloatField(default=0.00, verbose_name='Peso Lote')
    mcubtotallote = models.FloatField(default=0.00, verbose_name='Cubagem Lote')
    qtdvolumelote = models.FloatField(default=0.00, verbose_name='Valumes Lote')
    qtditemlote = models.FloatField(default=0.00, verbose_name='Items do Lote')
    seqordenacaoseparacao = models.IntegerField(verbose_name='Ordem Separação')
    seqpessoa = models.IntegerField(verbose_name='Código Cliente')
    qtdembsolcarga = models.FloatField(default=0.00, verbose_name='Qtd. Emb. Solic.')
    qtdembcarga = models.FloatField(default=0.00, verbose_name='Qtd. Emb.')
    qtdembsepcarga = models.FloatField(default=0.00, verbose_name='Qtd. Emb. Separada')
    nropedvenda = models.IntegerField(null=True, blank=True, verbose_name='Número Pedido')
    embalagem = models.CharField(max_length=5, default='', verbose_name='Unidade')
    peso = models.FloatField(default=0.00, verbose_name='Peso??')
    pesobruto = models.FloatField(default=0.00, verbose_name='Peso Bruto')
    pesoliquido = models.FloatField(default=0.00, verbose_name='Peso Líquido')
    altura = models.FloatField(default=0.00, verbose_name='Altura')
    largura = models.FloatField(default=0.00, verbose_name='Largura')
    profundidade = models.FloatField(default=0.00, verbose_name='Profundidade')
    volume = models.FloatField(default=0.00, verbose_name='volume')
    status = models.CharField(max_length=1, default='L', verbose_name='Status')
    insert_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Data')

    class Meta:
        db_table = 'consinco_cargas'
        verbose_name_plural = 'ConsincoCargas'

    def __str__(self):
        return f'carga:{self.nrocarga} lote:{self.seqlote} cliente:{self.seqpessoa} produto:{self.desccompleta}'


class LastCharge(models.Model):
    pk_last_charge = models.SmallIntegerField(primary_key=True, verbose_name='Código da Carga', default=1)
    fk_cargas_produtos = models.ForeignKey(CargasProdutos, default=0, on_delete=models.CASCADE, verbose_name='Cargas')
    fk_company = models.IntegerField(null=True, blank=True, verbose_name='Empresa')
    num_lot = models.IntegerField(null=True, blank=True, verbose_name='Lote')
    fk_product = models.IntegerField(null=True, blank=True, verbose_name='Produto')
    fk_customer = models.IntegerField(null=True, blank=True, verbose_name='Código Cliente')
    date_last_charge = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Data da Carga')

    class Meta:
        db_table = 'icity_last_charge'
        verbose_name_plural = 'Última Carga'

    def __str__(self):
        return f'{self.pk_last_charge} - Cliente: {self.fk_customer} - Produto: {self.fk_product}'


class Products(models.Model):
    pk_products = models.IntegerField(primary_key=True, verbose_name='Código')
    dsc_prod = models.CharField(max_length=50, verbose_name='Descrição')
    insert_date = models.DateTimeField(null=True, blank=True, verbose_name='Inserção')
    update_date = models.DateTimeField(null=True, blank=True, verbose_name='Atualização')

    class Meta:
        db_table = 'icity_products'
        verbose_name_plural = 'Produtos'

    def save(self, *args, **kwargs):
        if not self.insert_date:
            self.insert_date = timezone.now()
        self.update_date = timezone.now()
        return super(Products, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk_products} - {self.dsc_prod}'


class ProductsSimilar(models.Model):
    pk_products_similar = models.CharField(max_length=13, primary_key=True, verbose_name='Código de Barras')
    fk_products = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Código')
    street = models.CharField(max_length=3, verbose_name='Rua')
    tower = models.CharField(max_length=5, verbose_name='Predio')
    level = models.CharField(max_length=3, verbose_name='Nivel')
    position = models.CharField(max_length=5, verbose_name='Posicao')
    unity = models.CharField(max_length=5, verbose_name='Unidade')
    qtd_unity = models.FloatField(blank=True, default=0.00, verbose_name='QUant. da Unidade')
    volume = models.FloatField(blank=True, default=0.00, verbose_name='Volume')
    weight = models.FloatField(blank=True, default=0.00, verbose_name='Peso')
    height = models.FloatField(blank=True, default=0.00, verbose_name='Altura')
    width = models.FloatField(blank=True, default=0.00, verbose_name='Largura')
    depth = models.FloatField(blank=True, default=0.00, verbose_name='Profundidade')
    image_prod = models.TextField(blank=True, null=True, verbose_name='Imagem')     # Base64 decoded image (text)
    insert_date = models.DateTimeField(null=True, blank=True, verbose_name='Inserção')
    update_date = models.DateTimeField(null=True, blank=True, verbose_name='Atualização')

    class Meta:
        db_table = 'icity_products_similarity'
        verbose_name_plural = 'Produtos Similares'

    def save(self, *args, **kwargs):
        if not self.insert_date:
            self.insert_date = timezone.now()
        self.update_date = timezone.now()
        return super(ProductsSimilar, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.street} - {self.tower} - {self.pk_products_similar}'


class Carriers(models.Model):
    """
    Table that store all collects to do on 1 car
    """
    STATUS_OPTIONS = [
        ('L', 'Livre'),
        ('P', 'Processando'),
        ('S', 'Em Separação'),
        ('C', 'Em Conferência'),
    ]
    TYPE_LINE_OPTIONS = [
        ('AG', 'Alimetício Grandeza'),
        ('BF', 'Fardarias Grandeza'),
        ('BG', 'Bebidas Grandeza'),
        ('CO', 'Confinado'),
        ('FA', 'Fracionado Alimento'),
        ('FB', 'Fracionado Bebidas'),
        ('FF', 'Leveza Papel Higiênico'),
        ('FG', 'Fracionados Gerais'),
        ('FR', 'Fracionado Geral'),
        ('FL', 'Leveza Fardaria Grandeza'),
        ('LA', 'Licitação Alimento'),
        ('LF', 'Limpeza Fracionada'),
        ('LG', 'Limpeza Grandeza'),
        ('LL', 'Leveza Limpeza Grandeza'),
    ]
    # hash(charge, lot and fk_customers)
    pk_carriers = models.CharField(max_length=64, primary_key=True, verbose_name='Código Pedido')
    fk_customer = models.IntegerField(blank=True, default=0, verbose_name='Cod. Cliente')
    charge = models.IntegerField(verbose_name='Num. Carga')
    lot = models.IntegerField(verbose_name='Num Lote')
    weight_charge = models.FloatField(verbose_name='Peso')
    volume_charge = models.FloatField(verbose_name='Volume')
    flag_type_line = models.CharField(
        max_length=2, default='FG', choices=TYPE_LINE_OPTIONS, verbose_name='Tipo Separação'
    )
    flag_status = models.CharField(
        max_length=1, choices=STATUS_OPTIONS, default='L', verbose_name='Status')
    flag_ready = models.SmallIntegerField(default=0, verbose_name='Carregado')
    flag_conference = models.SmallIntegerField(default=0, verbose_name='Conferido')
    insert_date = models.DateTimeField(null=True, blank=True, verbose_name='Inserção')
    update_date = models.DateTimeField(null=True, blank=True, verbose_name='Atualização')

    class Meta:
        db_table = 'icity_carriers'
        verbose_name_plural = 'Pedidos'

    def save(self, *args, **kwargs):
        if not self.insert_date:
            self.insert_date = timezone.now()
        self.update_date = timezone.now()
        return super(Carriers, self).save(*args, **kwargs)

    def __str__(self):
        return f'carga:{self.charge} lote:{self.lot} cliente:{self.fk_customer}'


class CarriersProducts(models.Model):
    SIDE_OPTIONS = [
        ('E', 'Esquerda'),
        ('D', 'Direita'),
    ]
    # hash(charge, fk_customers, fk_products, street and tower)
    pk_carriers_products = models.CharField(
        max_length=64, default='', primary_key=True, verbose_name='Produtos do Pedido'
    )
    fk_carriers = models.ForeignKey(
        Carriers, default='', on_delete=models.PROTECT, verbose_name='Pedido'
    )
    fk_products = models.ForeignKey(
        Products, default='', on_delete=models.PROTECT, verbose_name='Produto'
    )
    fk_products_similar = models.ForeignKey(
        ProductsSimilar, on_delete=models.PROTECT,
        null=True, blank=True, max_length=13, verbose_name='Código de Barras'
    )
    street = models.CharField(default='', max_length=3, verbose_name='Rua')
    tower = models.CharField(default='', max_length=5, verbose_name='Predio')
    level = models.CharField(max_length=3, default=1, verbose_name='Nivel')
    position = models.CharField(max_length=5, default='0', verbose_name='Posicao')
    qtd_packing = models.FloatField(default=0.00, verbose_name='Quant. da Embalagem')
    qtd_order = models.FloatField(default=0.00, verbose_name='Quant. do Pedido')
    qtd_collected = models.FloatField(default=0.00, verbose_name='Quant. Coletada')
    unity = models.CharField(default='', max_length=2, verbose_name='UN')
    stock = models.FloatField(default=0.00, verbose_name='Estoque Atual')
    weight_prod = models.FloatField(default=0.00, verbose_name='Peso')
    volume_prod = models.FloatField(default=0.00, verbose_name='Volume')
    side = models.CharField(
        max_length=1, choices=SIDE_OPTIONS, default='E', verbose_name='Lado'
    )
    insert_date = models.DateTimeField(null=True, blank=True, verbose_name='Inserção')
    update_date = models.DateTimeField(null=True, blank=True, verbose_name='Atualização')

    class Meta:
        db_table = 'icity_carriers_products'
        verbose_name_plural = 'Produtos dos Pedidos'

    def save(self, *args, **kwargs):
        if not self.insert_date:
            self.insert_date = timezone.now()
        self.update_date = timezone.now()
        return super(CarriersProducts, self).save(*args, **kwargs)

    def __str__(self):
        return f'carga:{self.fk_carriers} Produto:{self.fk_products}'


class CarriersBoxes(models.Model):
    # has contendo pk_carriers_products, fk_users e fk_cars_boxes
    pk_carriers_boxes = models.CharField(max_length=64, primary_key=True, verbose_name='Box do Prod. Pedido')
    fk_carriers_products = models.ForeignKey(
        CarriersProducts, default='', on_delete=models.PROTECT, verbose_name='Carga'
    )
    fk_cars = models.ForeignKey(Cars, on_delete=models.PROTECT, verbose_name='Carro')
    fk_cars_boxes = models.ForeignKey(CarsBoxes, on_delete=models.PROTECT, verbose_name='Box')
    fk_users = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Operador')
    weight_box = models.FloatField(verbose_name='Peso')
    volume_box = models.FloatField(verbose_name='Volume m3')
    insert_date = models.DateTimeField(null=True, blank=True, verbose_name='Inserção')
    update_date = models.DateTimeField(null=True, blank=True, verbose_name='Atualização')

    class Meta:
        db_table = 'icity_carriers_boxes'
        verbose_name_plural = 'Boxes dos Pedidos'

    def save(self, *args, **kwargs):
        if not self.insert_date:
            self.insert_date = timezone.now()
        self.update_date = timezone.now()
        return super(CarriersBoxes, self).save(*args, **kwargs)

    def __str__(self):
        return f'carga:{self.fk_carriers_products} Box:{self.fk_cars_boxes} operador:{self.fk_users}'
