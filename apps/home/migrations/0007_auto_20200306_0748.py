# Generated by Django 3.0.1 on 2020-03-06 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_apihosts'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apihosts',
            options={'verbose_name_plural': 'hosts'},
        ),
        migrations.AlterModelOptions(
            name='carboxesmessage',
            options={'verbose_name_plural': 'Mensagens'},
        ),
        migrations.AlterModelOptions(
            name='cars',
            options={'verbose_name_plural': 'Carros'},
        ),
        migrations.AlterModelOptions(
            name='carsboxes',
            options={'verbose_name_plural': 'Boxes'},
        ),
    ]
