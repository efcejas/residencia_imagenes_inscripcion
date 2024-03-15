from django.db import models
from django.conf import settings
from django.utils import timezone

import datetime # Se importa para el ejemplo de la pregunta reciente

class Pregunta(models.Model):
    pregunta_texto = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField('Fecha de publicación')

    def __str__(self):
        # fecha_local = timezone.localtime(self.fecha_publicacion)
        return self.pregunta_texto # + " " + fecha_local.strftime('%d-%m-%Y %H:%M')

    def fue_publicada_recientemente(self):
        return self.fecha_publicacion >= timezone.now() - datetime.timedelta(days=1)

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_texto = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Opciones"