from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Residente, Usuario, RegistroAsistencia

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    ordering = ('username',)

class ResidenteAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'dni', 'fecha_nacimiento', 'matricula', 'telefono', 'fecha_de_ingreso')
    ordering = ('user__first_name', 'user__last_name')
    fieldsets = [
        ('Información personal', {'fields': ['dni', 'fecha_nacimiento', 'matricula', 'telefono', 'fecha_de_ingreso']}),
    ]
    search_fields = ('user__first_name', 'user__last_name', 'dni', 'matricula', 'telefono')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = 'user__first_name'  # Permite ordenar por este campo
    get_first_name.short_description = 'Nombre'  # Establece el nombre de la columna en la interfaz de administración

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.admin_order_field = 'user__last_name'  # Permite ordenar por este campo
    get_last_name.short_description = 'Apellido'  # Establece el nombre de la columna en la interfaz de administración

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Residente, ResidenteAdmin)

class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('residente','fecha', 'hora', 'llegada_a_tiempo', 'llegada_tarde', 'latitud', 'longitud')
    search_fields = ('residente__first_name', 'residente__last_name')

admin.site.register(RegistroAsistencia, RegistroAsistenciaAdmin)

