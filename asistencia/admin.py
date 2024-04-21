from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Docente, Residente, Usuario, Administrativo, RegistroAsistencia

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    ordering = ('username',)

class ResidenteAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'dni', 'fecha_nacimiento', 'matricula', 'telefono', 'fecha_de_ingreso')
    ordering = ('user__first_name', 'user__last_name')
    
    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = 'user__first_name'  # Permite ordenar por este campo
    get_first_name.short_description = 'Nombre'  # Establece el nombre de la columna en la interfaz de administración

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.admin_order_field = 'user__last_name'  # Permite ordenar por este campo
    get_last_name.short_description = 'Apellido'  # Establece el nombre de la columna en la interfaz de administración

class DocenteAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'get_email')
    ordering = ('user__first_name', 'user__last_name')

    def get_first_name(self, obj):
        return obj.user.first_name
    # Permite ordenar por este campo
    get_first_name.admin_order_field = 'user__first_name'
    # Establece el nombre de la columna en la interfaz de administración
    get_first_name.short_description = 'Nombre'

    def get_last_name(self, obj):
        return obj.user.last_name
    # Permite ordenar por este campo
    get_last_name.admin_order_field = 'user__last_name'
    # Establece el nombre de la columna en la interfaz de administración
    get_last_name.short_description = 'Apellido'

    def get_email(self, obj):
        return obj.user.email
    get_email.admin_order_field = 'user__email'  # Permite ordenar por este campo
    get_email.short_description = 'Correo electrónico'  # Establece el nombre de la columna en la interfaz de administración """

class AdministrativoAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'telefono')
    ordering = ('user__first_name', 'user__last_name')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = 'user__first_name'  # Permite ordenar por este campo
    get_first_name.short_description = 'Nombre'  # Establece el nombre de la columna en la interfaz de administración

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.admin_order_field = 'user__last_name'  # Permite ordenar por este campo
    get_last_name.short_description = 'Apellido'  # Establece el nombre de la columna en la interfaz de administración

class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('residente','fecha', 'hora', 'llegada_a_tiempo', 'llegada_tarde', 'latitud', 'longitud')
    search_fields = ('residente__first_name', 'residente__last_name')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Docente, DocenteAdmin)
admin.site.register(Residente, ResidenteAdmin)
admin.site.register(Administrativo, AdministrativoAdmin)
admin.site.register(RegistroAsistencia, RegistroAsistenciaAdmin)

