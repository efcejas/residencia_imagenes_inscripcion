from datetime import datetime, time, timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class Residente(AbstractUser):
    email = models.EmailField('Correo electrónico', blank=False, null=False, unique=True)
    dni = models.CharField('DNI', max_length=8, unique=True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento')
    matricula = models.CharField('Matrícula', max_length=6, unique=True)
    telefono = models.CharField('Teléfono', max_length=10)
    fecha_de_ingreso = models.DateField('Fecha de ingreso a la residencia')

    REQUIRED_FIELDS = ['email', 'dni', 'first_name', 'last_name', 'fecha_nacimiento', 'matricula', 'telefono', 'fecha_de_ingreso']

    class Meta:
        verbose_name = 'Residente'
        verbose_name_plural = 'Residentes'

    def clean(self):
        super().clean()
        self.first_name = self.first_name.title() if self.first_name else ''
        self.last_name = self.last_name.title() if self.last_name else ''
        self.email = BaseUserManager.normalize_email(self.email)  # Normaliza el email
    
    def __str__(self):
        return self.get_full_name()

class RegistroAsistencia(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField('Fecha y hora', auto_now_add=True)
    latitud = models.FloatField('Latitud')
    longitud = models.FloatField('Longitud')
    llegada_a_tiempo = models.BooleanField('¿Llegó a tiempo?', default=True)
    llegada_tarde = models.BooleanField('¿Llegó tarde?', default=False)

    class Meta:
        verbose_name = 'Registro de asistencia'
        verbose_name_plural = 'Registros de asistencia'

    def __str__(self):
        return f'{self.residente.get_full_name()}'
