from datetime import datetime, time, timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuario(AbstractUser):
    email = models.EmailField('Correo electrónico', blank=False, null=False, unique=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.get_full_name()

class Residente(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='residente_profile')
    dni = models.CharField('DNI', max_length=8, unique=True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento')
    matricula = models.CharField('Matrícula', max_length=6, unique=True)
    telefono = models.CharField('Teléfono', max_length=10)
    fecha_de_ingreso = models.DateField('Fecha de ingreso a la residencia')

    class Meta:
        verbose_name = 'Residente'
        verbose_name_plural = 'Residentes'

    def __str__(self):
        return self.user.get_full_name()

class Docente(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='docente_profile')

    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'

    def __str__(self):
        return self.user.get_full_name()

class Administrativo(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='administrativo_profile')
    telefono = models.CharField('Teléfono', max_length=10)

    class Meta:
        verbose_name = 'Administrativo'
        verbose_name_plural = 'Administrativos'

    def __str__(self):
        return self.user.get_full_name()

@receiver(post_save, sender=Usuario)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance, 'residente_profile'):
            Residente.objects.create(user=instance)
        elif hasattr(instance, 'docente_profile'):
            Docente.objects.create(user=instance)
        elif hasattr(instance, 'administrativo_profile'):
            Administrativo.objects.create(user=instance)

# Casi logro que el código funcione, pero me falta algo. ¿Qué es?

class RegistroAsistencia(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    fecha = models.DateField('Fecha', default=timezone.now)
    hora = models.TimeField('Hora', default='00:00')
    latitud = models.FloatField('Latitud')
    longitud = models.FloatField('Longitud')
    llegada_a_tiempo = models.BooleanField('¿Llegó a tiempo?', default=True)
    llegada_tarde = models.BooleanField('¿Llegó tarde?', default=False)

    class Meta:
        verbose_name = 'Registro de asistencia'
        verbose_name_plural = 'Registros de asistencia'

    def __str__(self):
        return f'{self.residente.get_full_name()}'
