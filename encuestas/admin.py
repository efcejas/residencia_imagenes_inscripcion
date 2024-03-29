from django.contrib import admin

# Register your models here.

from .models import Pregunta, Opcion

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 3

class PreguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['pregunta_texto']}),
        ('Información de fecha', {'fields': ['fecha_publicacion'], 'classes': ['collapse']}), # Se oculta por defecto
    ]
    inlines = [OpcionInline]
    list_display = ['pregunta_texto', 'fecha_publicacion', 'fue_publicada_recientemente']
    list_filter = ['fecha_publicacion']
    search_fields = ['pregunta_texto']

admin.site.register(Pregunta, PreguntaAdmin)
