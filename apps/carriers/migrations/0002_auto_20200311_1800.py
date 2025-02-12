# Generated by Django 3.0.1 on 2020-03-11 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carriers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carriers',
            name='insert_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Inserção'),
        ),
        migrations.AlterField(
            model_name='carriers',
            name='update_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Atualização'),
        ),
        migrations.AlterField(
            model_name='carriersboxes',
            name='insert_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Inserção'),
        ),
        migrations.AlterField(
            model_name='carriersboxes',
            name='update_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Atualização'),
        ),
        migrations.AlterField(
            model_name='carriersproducts',
            name='insert_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Inserção'),
        ),
        migrations.AlterField(
            model_name='carriersproducts',
            name='update_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Atualização'),
        ),
        migrations.AlterField(
            model_name='products',
            name='insert_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Inserção'),
        ),
        migrations.AlterField(
            model_name='products',
            name='update_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Atualização'),
        ),
        migrations.AlterField(
            model_name='productssimilar',
            name='insert_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Inserção'),
        ),
        migrations.AlterField(
            model_name='productssimilar',
            name='update_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Atualização'),
        ),
    ]
