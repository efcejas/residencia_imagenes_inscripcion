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
    llegada_tarde = models.BooleanField('¿Llegó tarde?', default=False)

    def save(self, *args, **kwargs):
        self.llegada_tarde = self.llego_tarde()
        super().save(*args, **kwargs)

    def llego_tarde(self):
        hora_inicio_clase = timezone.make_aware(datetime.combine(timezone.localtime().date(), time(23, 41)))
        hora_fin_clase = hora_inicio_clase + timedelta(minutes=5)  # Añadimos 5 minutos de tolerancia
        hora_actual = timezone.localtime().replace(second=0, microsecond=0)

        return hora_actual > hora_fin_clase  # Si la hora actual es estrictamente mayor que la hora de fin de la clase (hora de inicio + tolerancia), entonces el residente llegó tarde
    
    class Meta:
        verbose_name = 'Registro de asistencia'
        verbose_name_plural = 'Registros de asistencia'

    def __str__(self):
        return f'{self.residente.get_full_name()}'
