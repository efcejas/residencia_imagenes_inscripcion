# Importaciones de django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

# Configuración de la interfaz de administración

class CustomUserAdmin(UserAdmin):
    # Aquí puedes personalizar la interfaz de administración para los usuarios
    list_display = ('last_name','first_name','username', 'email', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

# Desregistra el administrador de usuarios predeterminado y registra el personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)