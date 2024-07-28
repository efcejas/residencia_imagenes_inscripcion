from django.db import models
from django.utils import timezone  # Para trabajar con fechas y horas
# Si necesitas relacionar tus modelos con el modelo de usuario
from django.contrib.auth.models import User
from django.urls import reverse  # Para obtener URLs de tus vistas
# Importa el modelo de etiquetas de la librería taggit
from taggit.managers import TaggableManager
# Importa el modelo de Sedes para relacionar con el modelo de Residentes
from asistencia.models import Sedes

# Crea tus modelos aquí.


class Paciente(models.Model):
    """
    Modelo que representa a un paciente.
    """
    nombre = models.CharField("Nombre del paciente", max_length=50)
    apellido = models.CharField("Apellido del paciente", max_length=50)
    dni = models.CharField("DNI del paciente", max_length=8,
                           unique=True, help_text="Ingrese el DNI sin puntos.")

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        self.nombre = ' '.join(word.capitalize()
                               for word in self.nombre.split())
        self.apellido = ' '.join(word.capitalize()
                                 for word in self.apellido.split())
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

class Patologia(models.Model):
    """
    Modelo que representa una patología.
    """
    nombre = models.CharField("Nombre de la patología", max_length=50, unique=True)

    class Meta:
        verbose_name = "Patología"
        verbose_name_plural = "Patologías"
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
        Paciente, on_delete=models.CASCADE, related_name='casos_interesantes')
    id_estudio = models.CharField("ID de estudio", max_length=50, unique=True, help_text="Cada estudio cuenta con un ID único que lo identifica y es asginado por cada equipo. Ingresando este ID se evitará duplicados.", error_messages={
                                  'unique': 'El ID de estudio ingresado ya existe en la base de datos.'})
    sede = models.ForeignKey(
        Sedes, on_delete=models.CASCADE, related_name='casos_interesantes')
    fecha = models.DateField("Fecha del caso", default=timezone.now,
                             help_text="Ingrese la fecha en la que se realizó el estudio.")
    tipo_estudio = models.CharField("Tipo de estudio", max_length=2, choices=OPCION_TIPO_ESTUDIO,
                                    help_text="Seleccione el tipo de estudio que se realizó.")
    contraste_ev = models.BooleanField(
        "Contraste", default=False, help_text="¿Se utilizó contraste endovenoso en el estudio?")
    contraste_or = models.BooleanField(
        "Contraste oral", default=False, help_text="¿Se utilizó contraste oral en el estudio?")
    region_anatomica = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='casos_interesantes', verbose_name="Región anatómica", help_text="Seleccione la región anatómica donde se encuentra la patología.")
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, related_name='casos_interesantes', help_text="Seleccione el sistema relacionado con la patología.")
    organo = models.ForeignKey(Organo, on_delete=models.CASCADE, related_name='casos_interesantes', help_text="Seleccione el órgano donde se encuentra la patología, si corresponde.")
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='casos_interesantes', help_text="Selecciona a que subespecialidad pertenece el caso.")
    descripcion = models.TextField(
        "Descripción del caso", help_text="Ingrese una breve descripción del caso.")
    hallazgos = models.ForeignKey(Patologia, on_delete=models.CASCADE, related_name='casos_interesantes', verbose_name="Hallazgos", help_text="Seleccione la patología que se encontró en el estudio.")
    fregmento_informe = models.TextField(
        "Fragmento del informe", help_text="Ingrese un fragmento del informe que menciona el hallazgo de interés o en el que se menciona el diagnóstico definitivo.")
    # imagenes_clave = models.ImageField("Imagen del caso", upload_to='casos_interesantes/', blank=True, null=True)
    etiquetas = TaggableManager("Etiquetas", help_text="Puede agregar etiquetas para facilitar la búsqueda de este caso. Separe las etiquetas con comas. Por ejemplo: neumonía, COVID-19, pulmón.", blank=True)

    class Meta:
        verbose_name = "Caso interesante"
        verbose_name_plural = "Casos interesantes"
        ordering = ['-fecha']

    def __str__(self):
        return f"Caso de {self.paciente} - {self.fecha}"
