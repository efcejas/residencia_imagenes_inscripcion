from django.contrib import admin
from .models import Empresa, Facturacion, Paciente, PacienteRegion, RegionEcografia, ValorRegionEmpresa, EstudioEspecial


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('nombre',)
    search_fields = ('nombre',)


class RegionEcografiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    ordering = ('nombre',)
    search_fields = ('nombre', 'descripcion')


class ValorRegionEmpresaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'region_ecografia', 'valor')
    ordering = ('empresa', 'region_ecografia')
    search_fields = ('empresa__nombre', 'region_ecografia__nombre')
    list_filter = ('empresa', 'region_ecografia')


class EstudioEspecialAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'region_ecografia', 'descripcion', 'valor')
    ordering = ('empresa', 'region_ecografia')
    search_fields = ('empresa__nombre', 'region_ecografia__nombre', 'descripcion')
    list_filter = ('empresa', 'region_ecografia', 'descripcion')


class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni')
    ordering = ('apellido', 'nombre')
    search_fields = ('nombre', 'apellido', 'dni')


class PacienteRegionAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'empresa', 'fecha', 'mostrar_regiones')  # Mostrar las regiones como método
    ordering = ('fecha',)
    search_fields = ('paciente__nombre', 'paciente__apellido', 'empresa__nombre')
    list_filter = ('paciente', 'empresa', 'fecha')

    # Método para mostrar las regiones asociadas a un paciente
    def mostrar_regiones(self, obj):
        return ", ".join([region.nombre for region in obj.regiones.all()])

    mostrar_regiones.short_description = 'Regiones'


class FacturacionAdmin(admin.ModelAdmin):
    list_display = ('paciente_region', 'valor_region_empresa', 'estudio_especial', 'fecha_facturacion', 'usuario', 'cantidad_regiones', 'total_facturado')
    ordering = ('fecha_facturacion',)
    search_fields = ('paciente_region__paciente__nombre', 'valor_region_empresa__empresa__nombre', 'usuario__username', 'estudio_especial__descripcion')
    list_filter = ('valor_region_empresa__empresa', 'usuario', 'fecha_facturacion', 'mes_facturacion', 'estudio_especial')

    # Mostrar el total facturado en la lista del admin
    def total_facturado(self, obj):
        return obj.total_facturado()
    total_facturado.short_description = 'Total Facturado (ARS)'


# Registrar los modelos en el admin
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(RegionEcografia, RegionEcografiaAdmin)
admin.site.register(ValorRegionEmpresa, ValorRegionEmpresaAdmin)
admin.site.register(EstudioEspecial, EstudioEspecialAdmin)  # Registrar el nuevo modelo
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(PacienteRegion, PacienteRegionAdmin)
admin.site.register(Facturacion, FacturacionAdmin)
