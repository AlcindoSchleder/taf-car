# Generated by Django 3.0.1 on 2020-02-17 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carriers', '0004_auto_20200217_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carriersproducts',
            name='mesano',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Mês/Ano'),
        ),
        migrations.AlterField(
            model_name='carriersproducts',
            name='peso',
            field=models.FloatField(default=0, verbose_name='Peso.'),
            preserve_default=False,
        ),
    ]
