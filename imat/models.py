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
        app_label = "imat"  # Para que Django pueda encontrar el modelo en la app 'imat'

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


# Modelo para almacenar información del residente
class Residente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    dni = models.CharField(max_length=15, unique=True, verbose_name="DNI")
    anio_residencia = models.CharField(
        help_text="Seleccione a qué año pertenece en la residencia",
        max_length=20,
        choices=[
            ('primer', 'Primer Año'),
            ('segundo', 'Segundo Año'),
            ('tercer', 'Tercer Año'),
            ('cuarto', 'Cuarto Año')
        ],
        default='primer',
        verbose_name="Año de residencia"
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"

    class Meta:
        verbose_name = "Residente"
        verbose_name_plural = "Residentes"

# Modelo para registrar los intentos de examen con nota
class ExamenRespuesta(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='examenes_respuestas', verbose_name="Residente")
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='respuestas', verbose_name="Examen")
    fecha_realizacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de realización")
    puntaje = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Puntaje")
    nivel = models.CharField(
        max_length=20,
        choices=[
            ('alto', 'Alto'),
            ('intermedio', 'Intermedio'),
            ('bajo', 'Bajo')
        ],
        blank=True,
        null=True,
        verbose_name="Nivel"
    )
    comentarios = models.TextField(blank=True, null=True, verbose_name="Comentarios del docente")

    def __str__(self):
        return f"Examen '{self.examen.titulo}' de {self.residente}"

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

# Modelo para registrar evaluaciones prácticas
class EvaluacionPractica(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='evaluaciones_practicas', verbose_name="Residente")
    fecha = models.DateField(default=timezone.now, verbose_name="Fecha de evaluación")
    puntaje = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Puntaje")
    nivel = models.CharField(
        max_length=20,
        choices=[
            ('alto', 'Alto'),
            ('intermedio', 'Intermedio'),
            ('bajo', 'Bajo')
        ],
        verbose_name="Nivel"
    )
    comentarios = models.TextField(blank=True, null=True, verbose_name="Comentarios del docente")

    def __str__(self):
        return f"Evaluación práctica de {self.residente} - {self.fecha}"

    class Meta:
        verbose_name = "Evaluación Práctica"
        verbose_name_plural = "Evaluaciones Prácticas"

# Modelo para el progreso del residente
class ProgresoResidente(models.Model):
    residente = models.OneToOneField(Residente, on_delete=models.CASCADE, related_name='progreso', verbose_name="Residente")
    puntaje_teorico_total = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Puntaje Teórico Total")
    puntaje_practico_total = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Puntaje Práctico Total")

    def __str__(self):
        return f"Progreso de {self.residente}"

    class Meta:
        verbose_name = "Progreso del Residente"
        verbose_name_plural = "Progresos de los Residentes"