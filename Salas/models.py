from django.db import models

# Create your models here.


class Reservas(models.Model):
    codigo = models.CharField(primary_key=True, max_length=4)
    fecha = models.DateField()
    inicio = models.TimeField()
    final = models.TimeField()
    sala = models.PositiveSmallIntegerField()
