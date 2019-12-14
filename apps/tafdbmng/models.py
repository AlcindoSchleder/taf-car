from django.db import models

# Create your models here.


class OracleFreights(models.Model):
    nrocarga = models.IntegerField(primary_key=True)


class Freights(models.Model):
    pk_freights = models.IntegerField(primary_key=True)


