from django.db import models
from django.utils import timezone

# Modelo para representar un examen
class Examen(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título del examen")
    descripcion = models.TextField(verbose_name="Descripción del examen")
    creado_en = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Examen"
        verbose_name_plural = "Exámenes"


# Modelo para representar cada pregunta del examen
class Pregunta(models.Model):
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='preguntas', verbose_name="Examen")
    texto = models.CharField(max_length=500, verbose_name="Texto de la pregunta")
    texto_ayuda = models.TextField(verbose_name="Texto de ayuda", blank=True)

    def __str__(self):
        return self.texto

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"


# Modelo para almacenar información del residente que realiza el examen
class Residente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    dni = models.CharField(max_length=15, unique=True, verbose_name="DNI")

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"

    class Meta:
        verbose_name = "Residente"
        verbose_name_plural = "Residentes"


# Nuevo modelo para registrar cada intento de examen realizado por un residente
class ExamenRespuesta(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='examenes', verbose_name="Residente")
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='respuestas', verbose_name="Examen")
    fecha_realizacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de realización")

    def __str__(self):
        return f"Examen '{self.examen.titulo}' realizado por {self.residente}"

    class Meta:
        verbose_name = "Examen Respuesta"
        verbose_name_plural = "Exámenes Respuestas"


# Modelo para almacenar las respuestas específicas de cada pregunta en un intento de examen
class Respuesta(models.Model):
    examen_respuesta = models.ForeignKey(ExamenRespuesta, on_delete=models.CASCADE, related_name='respuestas', verbose_name="Examen Respuesta", blank=True, null=True)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas', verbose_name="Pregunta")
    texto = models.TextField(verbose_name="Texto de la respuesta")
    creado_en = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")

    def __str__(self):
        return f"Respuesta a {self.pregunta.texto} - Examen de {self.examen_respuesta.residente}"

    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"

