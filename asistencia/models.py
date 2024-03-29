from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Residente(AbstractUser):
    dni = models.CharField('DNI', max_length=8, unique=True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento')
    matricula = models.CharField('Matrícula', max_length=6, unique=True)
    telefono = models.CharField('Teléfono', max_length=10)
    fecha_de_ingreso = models.DateField('Fecha de ingreso')

     # Cambia los nombres de los accesores inversos
    groups = models.ManyToManyField('auth.Group', related_name='residente_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='residente_user_permissions', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'dni', 'first_name', 'last_name', 'fecha_nacimiento', 'matricula', 'telefono', 'fecha_de_ingreso']

    class Meta:
        verbose_name = 'Residente'
        verbose_name_plural = 'Residentes'
    
    def __str__(self):
        return self.get_full_name()
