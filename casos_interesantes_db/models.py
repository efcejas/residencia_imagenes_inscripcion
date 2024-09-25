from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from asistencia.models import Sedes, Usuario

class Paciente(models.Model):
    """
    Modelo que representa a un paciente.
    """
    nombre = models.CharField("Nombre del paciente", max_length=50)
    apellido = models.CharField("Apellido del paciente", max_length=50)
    dni = models.CharField(
        "DNI del paciente", 
        max_length=8, 
        unique=True, 
        help_text="Ingrese el DNI sin puntos.", 
        error_messages={'unique': 'El DNI ingresado ya existe en la base de datos.' }
    )

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        self.nombre = ' '.join(word.capitalize() for word in self.nombre.split())
        self.apellido = ' '.join(word.capitalize() for word in self.apellido.split())
        return super().save(*args, **kwargs)

class Sistema(models.Model):
    """
    Modelo que representa un sistema del cuerpo humano.
    """
    nombre = models.CharField("Sistema", max_length=50, unique=True)

    class Meta:
        verbose_name = "Sistema"
        verbose_name_plural = "Sistemas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.capitalize()
        return super().save(*args, **kwargs)

class Organo(models.Model):
    """
    Modelo que representa un órgano.
    """
    nombre = models.CharField("Órgano", max_length=50, unique=True)

    class Meta:
        verbose_name = "Órgano"
        verbose_name_plural = "Órganos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.capitalize()
        return super().save(*args, **kwargs)

class Region(models.Model):
    """
    Modelo que representa una región anatómica.
    """
    nombre = models.CharField("Región de examen", max_length=50, unique=True)

    class Meta:
        verbose_name = "Región anatómica"
        verbose_name_plural = "Regiones anatómicas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.capitalize()
        return super().save(*args, **kwargs)

class Especialidad(models.Model):
    """
    Modelo que representa una especialidad.
    """
    nombre = models.CharField("Nombre de la especialidad", max_length=50, unique=True)

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.capitalize()
        return super().save(*args, **kwargs)

class CasoInteresante(models.Model):
    """
    Modelo que representa un caso interesante.
    """
    OPCION_TIPO_ESTUDIO = (
        ('RM', 'Resonancia magnética'),
        ('TC', 'Tomografía computada'),
        ('US', 'Ecografía'),
        ('RX', 'Radiografía'),
    )

    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        related_name='casos_interesantes'
    )
    
    id_estudio = models.CharField(
        "ID de estudio",
        max_length=50,
        unique=True,
        help_text=(
            "Cada caso debe contar con un ID único para evitar duplicados en la base de datos. "
            "El ID debe formarse tomando la fecha del estudio y la hora. "
            "Por ejemplo: para la fecha 12/05/2021 y la hora 14:30, el ID sería 120520211430."
        ),
        error_messages={'unique': 'El ID de estudio ingresado ya existe en la base de datos.'}
    )
    
    usuario_carga = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='casos_interesantes', 
        verbose_name="Usuario que cargó el caso"
    )
    
    sede = models.ForeignKey(
        Sedes, 
        on_delete=models.CASCADE, 
        related_name='casos_interesantes'
    )
    
    fecha = models.DateField(
        "Fecha del caso", 
        default=timezone.now, 
        help_text="Ingrese la fecha en la que se realizó el estudio."
    )
    
    tipo_estudio = models.CharField(
        "Tipo de estudio", 
        max_length=2, 
        choices=OPCION_TIPO_ESTUDIO, 
        help_text="Seleccione el tipo de estudio que se realizó."
    )
    
    contraste_ev = models.BooleanField(
        "Contraste endovenoso", 
        default=False, 
        help_text="¿Se utilizó contraste endovenoso en el estudio?"
    )
    
    contraste_or = models.BooleanField(
        "Contraste oral", 
        default=False, 
        help_text="¿Se utilizó contraste oral en el estudio?"
    )
    
    region_anatomica = models.ForeignKey(
        Region, 
        on_delete=models.CASCADE, 
        related_name='casos_interesantes', 
        verbose_name="Región anatómica", 
        help_text="Seleccione la región anatómica donde se encuentra la patología."
    )
    
    sistema = models.ForeignKey(
        Sistema, 
        on_delete=models.CASCADE, 
        related_name='casos_interesantes', 
        help_text="Seleccione el sistema relacionado con la patología."
    )
    
    organo = models.ForeignKey(
        Organo, 
        on_delete=models.CASCADE, 
        related_name='casos_interesantes', 
        help_text="Seleccione el órgano donde se encuentra la patología, si corresponde."
    )
    
    especialidad = models.ForeignKey(
        Especialidad, 
        on_delete=models.CASCADE, 
        related_name='casos_interesantes', 
        help_text="Selecciona a qué subespecialidad pertenece el caso."
    )
    
    descripcion = models.TextField(
        "Descripción del caso", 
        help_text="Ingrese una breve descripción del caso."
    )
    
    hallazgos = models.TextField(
        "Hallazgos", 
        help_text="Ingrese los hallazgos más relevantes del caso. Por ejemplo: Tumor en lóbulo superior derecho, Colangiocarcinoma, Neumonía bilateral, etc."
    )
    
    fregmento_informe = models.TextField(
        "Fragmento del informe", 
        help_text="Ingrese un fragmento del informe que menciona el hallazgo de interés o en el que se menciona el diagnóstico definitivo."
    )
    
    etiquetas = TaggableManager(
        "Etiquetas", 
        help_text="Puede agregar etiquetas para facilitar la búsqueda de este caso. Separe las etiquetas con comas. Por ejemplo: neumonía, COVID-19, pulmón.", 
        blank=True
    )

    class Meta:
        verbose_name = "Caso interesante"
        verbose_name_plural = "Casos interesantes"
        ordering = ['-fecha']

    def __str__(self):
        return f"Caso de {self.paciente} - {self.fecha}"

class ImagenCasoInteresante(models.Model):
    """
    Modelo que representa una imagen de un caso interesante.
    """
    caso = models.ForeignKey(
        CasoInteresante, 
        on_delete=models.CASCADE, 
        related_name='imagenes'
    )
    imagen = CloudinaryField('imagen')

    def __str__(self):
        return f"Imagen de {self.caso}"