from django.contrib import admin
from .models import Examen, Pregunta, Residente, Respuesta, ExamenRespuesta, EvaluacionPractica, ProgresoResidente

# Configuración para el modelo Examen en el panel de administración
class ExamenAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'creado_en')
    search_fields = ('titulo', 'descripcion')
    ordering = ('creado_en',)

# Configuración para el modelo Pregunta en el panel de administración
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('examen', 'texto')
    search_fields = ('texto', 'examen__titulo')
    ordering = ('examen',)

# Configuración para el modelo Residente en el panel de administración
class ResidenteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni')
    search_fields = ('nombre', 'apellido', 'dni')
    ordering = ('apellido', 'nombre')

# Configuración para el modelo ExamenRespuesta en el panel de administración
class ExamenRespuestaAdmin(admin.ModelAdmin):
    list_display = ('residente', 'examen', 'fecha_realizacion')
    search_fields = ('residente__nombre', 'residente__apellido', 'examen__titulo')
    ordering = ('fecha_realizacion',)
    list_filter = ('examen', 'fecha_realizacion')

# Configuración para el modelo Respuesta en el panel de administración
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('examen_respuesta', 'pregunta', 'texto', 'creado_en')
    search_fields = ('examen_respuesta__residente__nombre', 'examen_respuesta__residente__apellido', 'pregunta__texto', 'texto')
    ordering = ('creado_en',)
    list_filter = ('examen_respuesta__examen', 'pregunta')

# Configuración para el modelo EvaluacionPractica en el panel de administración
class EvaluacionPracticaAdmin(admin.ModelAdmin):
    list_display = ('residente', 'fecha', 'puntaje')
    search_fields = ('residente__nombre', 'residente__apellido', 'fecha')
    ordering = ('fecha',)

# Configuración para el modelo ProgresoResidente en el panel de administración
class ProgresoResidenteAdmin(admin.ModelAdmin):
    list_display = ('residente', 'puntaje_teorico_total', 'puntaje_practico_total')
    search_fields = ('residente__nombre', 'residente__apellido')
    ordering = ('residente',)

# Registrar los modelos en el sitio de administración
admin.site.register(Examen, ExamenAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Residente, ResidenteAdmin)
admin.site.register(ExamenRespuesta, ExamenRespuestaAdmin)
admin.site.register(Respuesta, RespuestaAdmin)
admin.site.register(EvaluacionPractica, EvaluacionPracticaAdmin)
admin.site.register(ProgresoResidente, ProgresoResidenteAdmin)
