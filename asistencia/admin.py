from django.contrib import admin

from .models import Residente

class ResidenteAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'dni', 'email')
    fieldsets = (
        ('Datos de la Cuenta', {'fields': ('username', 'password', 'email')}),
        ('Datos Personales', {'fields': ('first_name', 'last_name', 'fecha_nacimiento', 'dni')}),
        ('Datos de la Residencia', {'fields': ('matricula', 'fecha_de_ingreso')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

admin.site.register(Residente, ResidenteAdmin)
# Quiero darle formato al admin de django
