# Generated by Django 3.0.1 on 2020-03-11 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CargasProdutos',
            fields=[
                ('pk_cargas_produtos', models.AutoField(primary_key=True, serialize=False, verbose_name='Código de Acesso')),
                ('nroempresa', models.IntegerField(verbose_name='Empresa')),
                ('nrocarga', models.IntegerField(verbose_name='Carga')),
                ('seqlote', models.IntegerField(verbose_name='Lote')),
                ('seqtarefa', models.IntegerField(blank=True, null=True, verbose_name='Tarefa')),
                ('seqatividade', models.IntegerField(verbose_name='Aitividade')),
                ('seqproduto', models.IntegerField(verbose_name='Produto')),
                ('desccompleta', models.CharField(max_length=100, verbose_name='Descrição')),
                ('descreduzida', models.CharField(max_length=50, verbose_name='Descrição')),
                ('codrua', models.CharField(max_length=3, verbose_name='Rua')),
                ('nropredio', models.SmallIntegerField(verbose_name='Prédio')),
                ('nroapartamento', models.SmallIntegerField(verbose_name='Nível')),
                ('nrosala', models.SmallIntegerField(verbose_name='Local')),
                ('especieendereco', models.CharField(choices=[('A', 'Grandeza'), ('M', 'Miudeza')], max_length=1, verbose_name='Tipo End.')),
                ('indterreoaereo', models.CharField(choices=[('T', 'Térreo'), ('A', 'Aéreo')], max_length=1, verbose_name='Tipo Local')),
                ('qtdembalagem', models.FloatField(default=0.0, verbose_name='Qtd. Embalagem')),
                ('qtdatual', models.FloatField(default=0.0, verbose_name='Qtd. Atual')),
                ('statusendereco', models.CharField(choices=[('D', 'Disponível'), ('O', 'Ocupado'), ('B', 'Bloqueado'), ('R', 'Reservado'), ('I', 'Inativo'), ('E', 'Restrito'), ('Q', 'Quarentena')], max_length=1, verbose_name='Tipo Local')),
                ('tipespecie', models.CharField(blank=True, max_length=1, null=True, verbose_name='Tipo Espécie')),
                ('coddepossepar', models.SmallIntegerField(verbose_name='Depós. Separ.')),
                ('destino', models.CharField(max_length=40, verbose_name='Destino')),
                ('tipentrega', models.CharField(blank=True, max_length=1, null=True, verbose_name='Tipo Entrega')),
                ('mcubtotal', models.FloatField(default=0.0, verbose_name='Cubagem')),
                ('pesototal', models.FloatField(default=0.0, verbose_name='Peso')),
                ('nrobox', models.SmallIntegerField(verbose_name='Box do Lote')),
                ('statuscarga', models.CharField(choices=[('A', 'Aguardando'), ('F', 'Faturada'), ('G', 'Gerada'), ('L', 'Liberada'), ('S', 'Em Separação'), ('T', 'Termo de Liberação'), ('C', 'Gerando Carregamento'), ('X', 'Iniciado Processo de Cancelamento da Carga')], max_length=1, verbose_name='Status da Carga')),
                ('valorcarga', models.FloatField(default=0.0, verbose_name='Valor da Carga')),
                ('qtdembcargasep', models.FloatField(default=0.0, verbose_name='Qtd. Emb. Separ.')),
                ('qtdcontada', models.FloatField(default=0.0, verbose_name='Qtd. Emb. Contada')),
                ('qtdembsolcargasep', models.FloatField(default=0.0, verbose_name='Qtd. Emb. Carga Solic.')),
                ('qtdembsepcargasep', models.FloatField(default=0.0, verbose_name='Qtd. Emb. Carga Separ.')),
                ('codtipatividade', models.CharField(max_length=2, verbose_name='Código Atividade')),
                ('nroquebra', models.SmallIntegerField(verbose_name='Quebra')),
                ('mesano', models.CharField(blank=True, max_length=5, null=True, verbose_name='Mês/Ano')),
                ('metragemcubica', models.FloatField(default=0.0, verbose_name='Cubagem')),
                ('qtdvolume', models.FloatField(default=0.0, verbose_name='Volumnes')),
                ('qtditem', models.FloatField(default=0.0, verbose_name='Items')),
                ('indexclusao', models.CharField(max_length=1, verbose_name='Excluído')),
                ('grauprioridade', models.IntegerField(verbose_name='Prioridade')),
                ('statusrf', models.CharField(blank=True, max_length=1, null=True, verbose_name='Status RF')),
                ('statusatividade', models.CharField(choices=[('A', 'Aguardando'), ('E', 'Em Execução'), ('X', 'Cancelada'), ('F', 'Finalizada')], max_length=1, verbose_name='Status da Atividade')),
                ('tipseparacao', models.CharField(blank=True, choices=[('AG', 'Alimetício Grandeza'), ('BF', 'Fardarias Grandeza'), ('BG', 'Bebidas Grandeza'), ('CO', 'Confinado'), ('FA', 'Fracionado Alimento'), ('FB', 'Fracionado Bebidas'), ('FF', 'Leveza Papel Higiênico'), ('FR', 'Fracionado Alimento'), ('FG', 'Fracionado Gerais'), ('FL', 'Leveza Fardaria Grandeza'), ('LA', 'Licitação Alimento'), ('LF', 'Limpeza Fracionada'), ('LG', 'Limpeza Grandeza'), ('LL', 'Leveza Limpeza Grandeza')], max_length=2, null=True, verbose_name='Tipo Serpação')),
                ('tiplote', models.CharField(blank=True, max_length=2, null=True, verbose_name='Tipo Lote')),
                ('pesototallote', models.FloatField(default=0.0, verbose_name='Peso Lote')),
                ('mcubtotallote', models.FloatField(default=0.0, verbose_name='Cubagem Lote')),
                ('qtdvolumelote', models.FloatField(default=0.0, verbose_name='Valumes Lote')),
                ('qtditemlote', models.FloatField(default=0.0, verbose_name='Items do Lote')),
                ('seqordenacaoseparacao', models.IntegerField(verbose_name='Ordem Separação')),
                ('seqpessoa', models.IntegerField(verbose_name='Código Cliente')),
                ('qtdembsolcarga', models.FloatField(default=0.0, verbose_name='Qtd. Emb. Solic.')),
                ('qtdembcarga', models.FloatField(default=0.0, verbose_name='Qtd. Emb.')),
                ('qtdembsepcarga', models.FloatField(default=0.0, verbose_name='Qtd. Emb. Separada')),
                ('nropedvenda', models.IntegerField(blank=True, null=True, verbose_name='Número Pedido')),
                ('embalagem', models.CharField(default='', max_length=5, verbose_name='Unidade')),
                ('peso', models.FloatField(default=0.0, verbose_name='Peso??')),
                ('pesobruto', models.FloatField(default=0.0, verbose_name='Peso Bruto')),
                ('pesoliquido', models.FloatField(default=0.0, verbose_name='Peso Líquido')),
                ('altura', models.FloatField(default=0.0, verbose_name='Altura')),
                ('largura', models.FloatField(default=0.0, verbose_name='Largura')),
                ('profundidade', models.FloatField(default=0.0, verbose_name='Profundidade')),
                ('volume', models.FloatField(default=0.0, verbose_name='volume')),
                ('status', models.CharField(default='L', max_length=1, verbose_name='Status')),
                ('insert_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data')),
            ],
            options={
                'verbose_name_plural': 'ConsincoCargas',
                'db_table': 'consinco_cargas',
            },
        ),
        migrations.CreateModel(
            name='Carriers',
            fields=[
                ('pk_carriers', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='Código Pedido')),
                ('fk_customer', models.IntegerField(blank=True, default=0, verbose_name='Cod. Cliente')),
                ('charge', models.IntegerField(verbose_name='Num. Carga')),
                ('lot', models.IntegerField(verbose_name='Num Lote')),
                ('weight_charge', models.FloatField(verbose_name='Peso')),
                ('volume_charge', models.FloatField(verbose_name='Volume')),
                ('flag_type_line', models.CharField(choices=[('AG', 'Alimetício Grandeza'), ('BF', 'Fardarias Grandeza'), ('BG', 'Bebidas Grandeza'), ('CO', 'Confinado'), ('FA', 'Fracionado Alimento'), ('FB', 'Fracionado Bebidas'), ('FF', 'Leveza Papel Higiênico'), ('FG', 'Fracionados Gerais'), ('FR', 'Fracionado Geral'), ('FL', 'Leveza Fardaria Grandeza'), ('LA', 'Licitação Alimento'), ('LF', 'Limpeza Fracionada'), ('LG', 'Limpeza Grandeza'), ('LL', 'Leveza Limpeza Grandeza')], default='FG', max_length=2, verbose_name='Tipo Separação')),
                ('flag_status', models.CharField(choices=[('L', 'Livre'), ('P', 'Processando'), ('S', 'Em Separação'), ('C', 'Em Conferência')], default='L', max_length=1, verbose_name='Status')),
                ('flag_ready', models.SmallIntegerField(default=0, verbose_name='Carregado')),
                ('flag_conference', models.SmallIntegerField(default=0, verbose_name='Conferido')),
                ('insert_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Inserção')),
                ('update_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualização')),
            ],
            options={
                'verbose_name_plural': 'Pedidos',
                'db_table': 'icity_carriers',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('pk_products', models.IntegerField(primary_key=True, serialize=False, verbose_name='Código')),
                ('dsc_prod', models.CharField(max_length=50, verbose_name='Descrição')),
                ('insert_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Inserção')),
                ('update_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualização')),
            ],
            options={
                'verbose_name_plural': 'Produtos',
                'db_table': 'icity_products',
            },
        ),
        migrations.CreateModel(
            name='ProductsSimilar',
            fields=[
                ('pk_products_similar', models.CharField(max_length=13, primary_key=True, serialize=False, verbose_name='Código de Barras')),
                ('street', models.CharField(max_length=3, verbose_name='Rua')),
                ('tower', models.CharField(max_length=5, verbose_name='Predio')),
                ('level', models.CharField(max_length=3, verbose_name='Nivel')),
                ('position', models.CharField(max_length=5, verbose_name='Posicao')),
                ('unity', models.CharField(max_length=5, verbose_name='Unidade')),
                ('qtd_unity', models.FloatField(blank=True, default=0.0, verbose_name='QUant. da Unidade')),
                ('volume', models.FloatField(blank=True, default=0.0, verbose_name='Volume')),
                ('weight', models.FloatField(blank=True, default=0.0, verbose_name='Peso')),
                ('height', models.FloatField(blank=True, default=0.0, verbose_name='Altura')),
                ('width', models.FloatField(blank=True, default=0.0, verbose_name='Largura')),
                ('depth', models.FloatField(blank=True, default=0.0, verbose_name='Profundidade')),
                ('image_prod', models.TextField(blank=True, null=True, verbose_name='Imagem')),
                ('insert_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Inserção')),
                ('update_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualização')),
                ('fk_products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carriers.Products', verbose_name='Código')),
            ],
            options={
                'verbose_name_plural': 'Produtos Similares',
                'db_table': 'icity_products_similarity',
            },
        ),
        migrations.CreateModel(
            name='LastCharge',
            fields=[
                ('pk_last_charge', models.SmallIntegerField(default=1, primary_key=True, serialize=False, verbose_name='Código da Carga')),
                ('fk_company', models.IntegerField(blank=True, null=True, verbose_name='Empresa')),
                ('num_lot', models.IntegerField(blank=True, null=True, verbose_name='Lote')),
                ('fk_product', models.IntegerField(blank=True, null=True, verbose_name='Produto')),
                ('fk_customer', models.IntegerField(blank=True, null=True, verbose_name='Código Cliente')),
                ('date_last_charge', models.DateTimeField(auto_now=True, null=True, verbose_name='Data da Carga')),
                ('fk_cargas_produtos', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='carriers.CargasProdutos', verbose_name='Cargas')),
            ],
            options={
                'verbose_name_plural': 'Última Carga',
                'db_table': 'icity_last_charge',
            },
        ),
        migrations.CreateModel(
            name='CarriersProducts',
            fields=[
                ('pk_carriers_products', models.CharField(default='', max_length=64, primary_key=True, serialize=False, verbose_name='Produtos do Pedido')),
                ('street', models.CharField(default='', max_length=3, verbose_name='Rua')),
                ('tower', models.CharField(default='', max_length=5, verbose_name='Predio')),
                ('level', models.CharField(default=1, max_length=3, verbose_name='Nivel')),
                ('position', models.CharField(default='0', max_length=5, verbose_name='Posicao')),
                ('qtd_packing', models.FloatField(default=0.0, verbose_name='Quant. da Embalagem')),
                ('qtd_order', models.FloatField(default=0.0, verbose_name='Quant. do Pedido')),
                ('qtd_collected', models.FloatField(default=0.0, verbose_name='Quant. Coletada')),
                ('unity', models.CharField(default='', max_length=2, verbose_name='UN')),
                ('stock', models.FloatField(default=0.0, verbose_name='Estoque Atual')),
                ('weight_prod', models.FloatField(default=0.0, verbose_name='Peso')),
                ('volume_prod', models.FloatField(default=0.0, verbose_name='Volume')),
                ('side', models.CharField(choices=[('E', 'Esquerda'), ('D', 'Direita')], default='E', max_length=1, verbose_name='Lado')),
                ('insert_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Inserção')),
                ('update_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualização')),
                ('fk_carriers', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='carriers.Carriers', verbose_name='Pedido')),
                ('fk_products', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='carriers.Products', verbose_name='Produto')),
                ('fk_products_similar', models.ForeignKey(blank=True, max_length=13, null=True, on_delete=django.db.models.deletion.PROTECT, to='carriers.ProductsSimilar', verbose_name='Código de Barras')),
            ],
            options={
                'verbose_name_plural': 'Produtos dos Pedidos',
                'db_table': 'icity_carriers_products',
            },
        ),
        migrations.CreateModel(
            name='CarriersBoxes',
            fields=[
                ('pk_carriers_boxes', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='Box do Prod. Pedido')),
                ('weight_box', models.FloatField(verbose_name='Peso')),
                ('volume_box', models.FloatField(verbose_name='Volume m3')),
                ('insert_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Inserção')),
                ('update_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Atualização')),
                ('fk_carriers_products', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='carriers.CarriersProducts', verbose_name='Carga')),
                ('fk_cars', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.Cars', verbose_name='Carro')),
                ('fk_cars_boxes', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.CarsBoxes', verbose_name='Box')),
                ('fk_users', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Operador')),
            ],
            options={
                'verbose_name_plural': 'Boxes dos Pedidos',
                'db_table': 'icity_carriers_boxes',
            },
        ),
    ]
