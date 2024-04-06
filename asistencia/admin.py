from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Residente, RegistroAsistencia

class ResidenteAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Campos personalizados', {'fields': ('dni', 'fecha_nacimiento', 'matricula', 'telefono', 'fecha_de_ingreso')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos personalizados', {'fields': ('email', 'dni', 'fecha_nacimiento', 'matricula', 'telefono', 'fecha_de_ingreso')}),
    )

admin.site.register(Residente, ResidenteAdmin)

class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('residente', 'fecha_hora', 'llegada_tarde', 'latitud', 'longitud')
    search_fields = ('residente__first_name', 'residente__last_name')

admin.site.register(RegistroAsistencia, RegistroAsistenciaAdmin)

