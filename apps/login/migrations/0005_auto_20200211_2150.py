# Generated by Django 3.0.1 on 2020-02-12 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20200211_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersoperators',
            name='insert_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data e Hora da Inserção'),
        ),
    ]
