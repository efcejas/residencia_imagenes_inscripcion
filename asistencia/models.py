from datetime import datetime, time, timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Modelos relacionados con la autenticación de usuarios

class Usuario(AbstractUser):
    email = models.EmailField('Correo electrónico', blank=False, null=False, unique=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        # Normaliza el nombre y el apellido
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()

        # Normaliza el email
        email_username, domain = self.email.rsplit('@', 1)
        self.email = email_username + '@' + domain.lower()

        super().save(*args, **kwargs)

class Residente(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='residente_profile')
    dni = models.CharField('DNI', max_length=8, unique=True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento')
    matricula = models.CharField('Matrícula', max_length=6, unique=True)
    telefono = models.CharField('Teléfono', max_length=10)
    fecha_de_ingreso = models.DateField('Fecha de ingreso a la residencia')

    class Meta:
        verbose_name = 'Residente'
        verbose_name_plural = 'Residentes'

    def __str__(self):
        return self.user.get_full_name()

    def dni_con_puntos(self):
        try:
            return "{:,}".format(int(self.dni)).replace(",", ".")
        except ValueError:
            return self.dni

    def matricula_con_puntos(self):
        try:
            return "{:,}".format(int(self.matricula)).replace(",", ".")
        except ValueError:
            return self.matricula

class Docente(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='docente_profile')

    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'

    def __str__(self):
        return self.user.get_full_name()

class Administrativo(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='administrativo_profile')
    telefono = models.CharField('Teléfono', max_length=10)

    class Meta:
        verbose_name = 'Administrativo'
        verbose_name_plural = 'Administrativos'

    def __str__(self):
        return self.user.get_full_name()

@receiver(post_save, sender=Usuario)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance, 'residente_profile'):
            Residente.objects.create(user=instance)
        elif hasattr(instance, 'docente_profile'):
            Docente.objects.create(user=instance)
        elif hasattr(instance, 'administrativo_profile'):
            Administrativo.objects.create(user=instance)

# Modelos relacionados con la asistencia de los residentes

class RegistroAsistencia(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    fecha = models.DateField('Fecha', default=timezone.now)
    hora = models.TimeField('Hora', default='00:00')
    latitud = models.FloatField('Latitud')
    longitud = models.FloatField('Longitud')
    llegada_a_tiempo = models.BooleanField('¿Llegó a tiempo?', default=True)
    llegada_tarde = models.BooleanField('¿Llegó tarde?', default=False)

    class Meta:
        verbose_name = 'Registro de asistencia'
        verbose_name_plural = 'Registros de asistencia'

    def __str__(self):
        return f'Registro de asistencia para Residente {self.residente}'

# Modelos relacionados con la gestión de grupos 

class GruposResidentes(models.Model):
    OPCIONES_RESIDENCIAS = [
        ('DM', 'Diagnóstico Médico'),
        ('IM', 'Investigaciones Médicas'),
        ('FV', 'Fundación Favaloro'),
        ('US', 'Universidad del Salvador'),
    ]

    OPCIONES_AÑO = [
        ('R1', 'Primer año'),
        ('R2', 'Segundo año'),
        ('R3', 'Tercer año'),
        ('R4', 'Cuarto año'),
    ]
       
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, help_text='Seleccione al residente que quiere asignar a un grupo')
    residencia = models.CharField('Residencia', max_length=20, choices=OPCIONES_RESIDENCIAS, help_text='Seleccione la residencia a la que pertenece el residente')
    año = models.CharField('Año', max_length=20, choices=OPCIONES_AÑO, help_text='Seleccione el año en el que se encuentra el residente')

    class Meta:
        verbose_name = 'Residentes'
        verbose_name_plural = 'Residentes por año y residencia'

    def __str__(self):
        return f'{self.residente} - {self.residencia} - {self.año}'
        
# Modelos relacionados con la evaluación de los residentes

class EvaluacionPeriodica(models.Model):
    OPCION_NOTA = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    ]

    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, verbose_name='Residente')
    evaluador = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Evaluador')
    aspecto_positivo = models.TextField('Aspecto positivo', blank=True, max_length=600)
    aspecto_negativo = models.TextField('Aspecto negativo', blank=True, max_length=600)
    nota = models.IntegerField('Nota', choices=OPCION_NOTA)
    fecha = models.DateField('Fecha', default=timezone.now)

    class Meta:
        verbose_name = 'Evaluación periódica'
        verbose_name_plural = 'Evaluaciones periódicas'
        unique_together = ['residente', 'evaluador', 'fecha']
    
    def __str__(self):
        return f'{self.residente} - Aspecto positivo: {self.aspecto_positivo} - Aspecto negativo: {self.aspecto_negativo} - Nota: {self.nota} - Fecha de evaluación: {self.fecha} - evaluador: {self.evaluador}'

# Modelos relacionados con material de estudio y actividades académicas

class DisertantesClases(models.Model):
    nombre_disertante = models.CharField('Nombre del disertante', max_length=100)
    apellido_disertante = models.CharField('Apellido del disertante', max_length=100)

    class Meta:
        verbose_name = 'Disertante'
        verbose_name_plural = 'Disertantes'

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.nombre_disertante} {self.apellido_disertante}"

class ClasificacionTematica(models.Model):
    OPCION_SECCIONES = [
        ('A', 'Abdomen'),
        ('CV', 'Cardiovascular'),
        ('MSK', 'Musculoesquelético'),
        ('N', 'Neuroradiología'),
        ('O', 'Obstetricia'),
        ('IP', 'Imágenes pediátricas'),
        ('UR', 'Uroradiología y genitales masculinos'),
        ('IM', 'Imágenes mamarias'),
        ('CC', 'Cabeza y cuello'),
        ('T', 'Tórax'),
        ('OR', 'Oncoloradiología'),
        ('IR', 'Intervencionismo'),
        ('N', 'Nuclear'),
        ('GIN', 'Ginecología'),
        ('OT', 'Otras'),
    ]

    seccion = models.CharField('Sección', max_length=20, choices=OPCION_SECCIONES, unique=True, error_messages={'unique': 'Esa sección ya está registrada.'})

    class Meta:
        verbose_name = 'Clasificación temática'
        verbose_name_plural = 'Clasificaciones temáticas'

    def __str__(self):
        return self.get_seccion_display()

class ClasesVideos(models.Model):
    titulo = models.CharField('Título', max_length=100)
    disertante = models.ForeignKey(DisertantesClases, on_delete=models.CASCADE, null=True, blank=True, related_name='videos')
    vimeo_url = models.URLField('URL de Vimeo', max_length=200, unique=True, error_messages={'unique': 'Ese video ya está registrado.'})
    fecha_publicacion = models.DateField('Fecha de publicación', default=timezone.now)
    descripcion = models.TextField('Descripción', null=True, blank=True, max_length=200)
    clasificaciones_tematicas = models.ManyToManyField(ClasificacionTematica, related_name='videos')

    class Meta:
        verbose_name = 'Clase'
        verbose_name_plural = 'Videos de clases'

    def __str__(self):
        return self.titulo

    def embed_url(self):
        return self.vimeo_url.replace('https://vimeo.com/', 'https://player.vimeo.com/video/')

# Otros modelos a organizar. 

class Sedes(models.Model):
    nombre_sede = models.CharField(max_length=100, unique=True, error_messages={'unique': 'Esa sede ya está registrada.'})
    direccion = models.CharField(max_length=100, unique=True, error_messages={'unique': 'Ya existe una sede registrada con esa dirección.'})
    telefono = models.CharField('Teléfono', max_length=15)
    referente = models.CharField('Referente', max_length=50)

    class Meta:
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'

    def save(self, *args, **kwargs):
        # Normaliza el nombre de la sede
        self.nombre_sede = self.nombre_sede.title()

        # Normaliza la dirección
        self.direccion = self.direccion.title()

        # Normaliza el nombre del referente
        self.referente = self.referente.title()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_sede + ' - ' + self.direccion

class Aulas(models.Model):
    OPCION_AULA = [
        ('DM', 'Diagnóstico Médico'),
        ('IM', 'Investigaciones Médicas'),
    ]

    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE)
    nombre_aula = models.CharField('Nombre del aula', max_length=50, choices=OPCION_AULA)
    latitud = models.FloatField('Latitud')
    longitud = models.FloatField('Longitud')

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
    
    def __str__(self):
        return f'{self.nombre_aula} - {self.sede} - {self.sede.direccion}'

""" class CalendarioActividadesAcademicas(models.Model):
    OPCIONES_ACTIVIDADES = [
        ('Ateneo', 'Ateneo')
        ('Clase', 'Clase'),
        ('Examen', 'Examen'),
        ('Entrega', 'Entrega de trabajos'),
        ('Otro', 'Otro'),
    ]

    OPCIONES_DIAS = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    OPCIONES_HORAS = [
        ('07:00', '07:00'),
        ('08:00', '08:00'),
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('21:00', '21:00'),
        ('22:00', '22:00'),
    ]

    aula = models.ForeignKey(Aulas, on_delete=models.CASCADE)
    actividad = models.CharField('Actividad', max_length=20, choices=OPCIONES_ACTIVIDADES)
    dia = models.CharField('Día', max_length=20, choices=OPCIONES_DIAS)
    hora = models.CharField('Hora', max_length=20, choices=OPCIONES_HORAS)
    fecha = models.DateField('Fecha', default=timezone.now)
    descripcion = models.TextField('Descripción', max_length=200)

    class Meta:
        verbose_name = 'Actividad académica'
        verbose_name_plural = 'Calendario de actividades académicas'

    def __str__(self):
        return f'{self.actividad} - {self.dia} - {self.hora} - {self.fecha}'
 """
