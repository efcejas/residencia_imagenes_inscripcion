from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Asistencia(models.Model):
    residente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=100)