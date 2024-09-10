from django.contrib import admin
from .models import Paciente, Organo, Sistema, Region, Especialidad, CasoInteresante, ImagenCasoInteresante

# Registra tus modelos aquí.
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni')
    ordering = ('apellido', 'nombre')
    search_fields = ('nombre', 'apellido', 'dni')
    list_filter = ('apellido', 'dni')

class OrganoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('nombre',)
    search_fields = ('nombre',)

class SistemaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('nombre',)
    search_fields = ('nombre',)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('nombre',)
    search_fields = ('nombre',)

class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('nombre',)
    search_fields = ('nombre',)

class CasoInteresanteAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha', 'sistema', 'organo', 'region_anatomica', 'especialidad')
    ordering = ('fecha',)
    search_fields = ('paciente__nombre', 'paciente__apellido', 'sistema__nombre', 'organo__nombre', 'region_anatomica__nombre', 'especialidad__nombre')
    list_filter = ('sistema', 'organo', 'region_anatomica', 'especialidad')

class ImagenCasoInteresanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'caso', 'imagen')
    search_fields = ('caso__nombre',)
    list_filter = ('caso',)

admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Organo, OrganoAdmin)
admin.site.register(Sistema, SistemaAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(CasoInteresante, CasoInteresanteAdmin)
admin.site.register(ImagenCasoInteresante, ImagenCasoInteresanteAdmin)
