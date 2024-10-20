from django.db import models
from django.contrib.auth.models import User
from asistencia.models import Usuario
from datetime import datetime


class Empresa(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class RegionEcografia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Región de ecografía"
        verbose_name_plural = "Regiones de ecografía"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class ValorRegionEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    region_ecografia = models.ForeignKey(RegionEcografia, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Valor por región y empresa"
        verbose_name_plural = "Valores por región y empresa"
        unique_together = ('empresa', 'region_ecografia')

    def __str__(self):
        return f"{self.empresa} - {self.region_ecografia} - {self.valor}"


class EstudioEspecial(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    region_ecografia = models.ForeignKey(RegionEcografia, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)  # Descripción del estudio especial
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor del estudio especial

    class Meta:
        verbose_name = "Estudio Especial"
        verbose_name_plural = "Estudios Especiales"
        unique_together = ('empresa', 'region_ecografia', 'descripcion')  # Se garantiza que un estudio especial sea único por empresa y región

    def __str__(self):
        return f"{self.empresa} - {self.region_ecografia} ({self.descripcion}) - {self.valor}"


class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class PacienteRegion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    regiones = models.ManyToManyField(RegionEcografia)  # Relación muchos a muchos: un paciente puede tener varias regiones
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Regiones por paciente"
        verbose_name_plural = "Regiones por pacientes"
        ordering = ['fecha']

    def __str__(self):
        return f"{self.paciente} - {self.empresa} - {self.fecha}"


class Facturacion(models.Model):
    paciente_region = models.ForeignKey(PacienteRegion, on_delete=models.CASCADE, null=True, blank=True)
    valor_region_empresa = models.ForeignKey(ValorRegionEmpresa, on_delete=models.CASCADE, null=True, blank=True)  # Valor base
    estudio_especial = models.ForeignKey(EstudioEspecial, on_delete=models.CASCADE, null=True, blank=True)  # Estudio especial opcional
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Médico responsable
    fecha_facturacion = models.DateField(auto_now_add=True)
    cantidad_regiones = models.PositiveIntegerField(default=1)
    mes_facturacion = models.CharField(max_length=7, editable=False, default=datetime.now().strftime('%Y-%m'))

    class Meta:
        verbose_name = "Facturación"
        verbose_name_plural = "Facturaciones"
        ordering = ['fecha_facturacion']

    def total_facturado(self):
        # Si hay un estudio especial, usar ese valor, de lo contrario usar el valor base
        if self.estudio_especial:
            return self.estudio_especial.valor * self.cantidad_regiones
        return self.valor_region_empresa.valor * self.cantidad_regiones

    def save(self, *args, **kwargs):
        # Almacenar el mes de la facturación en formato "YYYY-MM"
        self.mes_facturacion = self.fecha_facturacion.strftime('%Y-%m')
        super().save(*args, **kwargs)

    def __str__(self):
        if self.estudio_especial:
            return f"{self.paciente_region.paciente} - {self.estudio_especial.empresa} ({self.estudio_especial.descripcion}) - Total: {self.total_facturado()}"
        return f"{self.paciente_region.paciente} - {self.valor_region_empresa.empresa} - Total: {self.total_facturado()}"


