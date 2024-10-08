from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Docente, Residente, Usuario, Administrativo, RegistroAsistencia, Sedes, GruposResidentes, Aulas, EvaluacionPeriodica, ClasesVideos, DisertantesClases, ClasificacionTematica, ConteoVisitaPagina, ConteoVisualizacionVideo, AteneoEvaluacion

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    ordering = ('username',)

class ResidenteAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'dni_con_puntos', 'fecha_nacimiento', 'matricula_con_puntos', 'telefono', 'fecha_de_ingreso')
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

class SedesAdmin(admin.ModelAdmin):
    list_display = ('nombre_sede', 'direccion', 'telefono', 'referente')
    ordering = ('nombre_sede',)

class GruposResidentesAdmin(admin.ModelAdmin):
    list_display = ('residente', 'residencia', 'año')  # Los campos que quieres mostrar en la lista
    search_fields = ('residente__user__first_name', 'residente__user__last_name', 'residencia', 'año')  # Los campos por los que quieres buscar
    list_filter = ('residencia', 'año')  # Los campos por los que quieres filtrar
    ordering = ('residente__user__first_name', 'residente__user__last_name')  # El orden en que quieres mostrar los registros

class AulasAdmin(admin.ModelAdmin):
    list_display = ('nombre_aula', 'get_nombre_sede', 'get_direccion_sede',)
    ordering = ('nombre_aula',)

    def get_nombre_sede(self, obj):
        return obj.sede.nombre_sede  # Retorna el nombre de la sede
    get_nombre_sede.short_description = 'Sede'  # Etiqueta para la columna

    def get_direccion_sede(self, obj):
        return obj.sede.direccion  # Retorna la direccion de la sede
    get_direccion_sede.short_description = 'Dirección'  # Etiqueta para la columna

# Registro de los modelos relacionados con evaluaciones

class AteneoEvaluacionAdmin(admin.ModelAdmin):
    list_display = ('ateneo_fecha', 'user', 'nota_general', 'comentario_aprendizaje',)
    ordering = ('ateneo_fecha', 'user',) 

class EvaluacionPeriodicaAdmin(admin.ModelAdmin):
    list_display = ('residente', 'aspecto_positivo', 'aspecto_negativo', 'nota', 'fecha', 'evaluador',)
    ordering = ('residente', 'fecha', 'evaluador',)

# Registro de los modelos relacionados con material de estudio y actividades académicas

class DisertantesClasesAdmin(admin.ModelAdmin):
    list_display = ('nombre_disertante', 'apellido_disertante',)
    ordering = ('nombre_disertante', 'apellido_disertante',)

class ClasificacionTematicaAdmin(admin.ModelAdmin):
    list_display = ('seccion',)
    ordering = ('seccion',)

class ClasesVideosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'vimeo_url', 'disertante', 'fecha_publicacion')
    ordering = ('titulo',)
    list_filter = ('disertante', 'clasificaciones_tematicas')
    search_fields = ('titulo', 'disertante__nombre_disertante', 'disertante__apellido_disertante', 'clasificaciones_tematicas__seccion')
    filter_horizontal = ('clasificaciones_tematicas',)  # Esto permite selección múltiple

# Registro de los modelos relacionados con el conteo de visitas y visualizaciones

class ConteoVisitaPaginaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_visita')
    ordering = ('usuario' , '-fecha_visita')

class ConteoVisualizacionVideoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'video', 'fecha_visualizacion')
    ordering = ('usuario' , '-fecha_visualizacion')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Docente, DocenteAdmin)
admin.site.register(Residente, ResidenteAdmin)
admin.site.register(Administrativo, AdministrativoAdmin)
admin.site.register(RegistroAsistencia, RegistroAsistenciaAdmin)
admin.site.register(Sedes, SedesAdmin)
admin.site.register(GruposResidentes, GruposResidentesAdmin)
admin.site.register(Aulas, AulasAdmin)
admin.site.register(EvaluacionPeriodica, EvaluacionPeriodicaAdmin)
admin.site.register(ClasesVideos, ClasesVideosAdmin)
admin.site.register(DisertantesClases, DisertantesClasesAdmin)
admin.site.register(ClasificacionTematica, ClasificacionTematicaAdmin)
admin.site.register(ConteoVisitaPagina, ConteoVisitaPaginaAdmin)
admin.site.register(ConteoVisualizacionVideo, ConteoVisualizacionVideoAdmin)
admin.site.register(AteneoEvaluacion, AteneoEvaluacionAdmin)



