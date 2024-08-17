from django.urls import path
from django.views.generic import TemplateView
from .views import RegistroAsistenciaView, ListaAsistenciaView, SedesCreateView, SedesListView, SedeUpdateView, SedeDeleteView, ResidentesListView, CalcularWashoutView, PerfilView, RegistroAsistenciaFiltradoListView, EvaluacionPeriodicaCreateView, ClasesVideosListView, EvaluadosListView, EvaluadosDetailView, AteneoEvaluacionCreateView, AteneoEvaluacionListView
from . import views

app_name = "asistencia"
urlpatterns = [
    # Rutas relacionadas con la asistencia
    path('registro_asistencia/', RegistroAsistenciaView.as_view(), name='registro_asistencia'),  # Vista para registrar la asistencia
    path('asistencias_registradas/', ListaAsistenciaView.as_view(), name='asistencias_registradas'),  # Vista para listar las asistencias registradas
    path('control_asistencia/', RegistroAsistenciaFiltradoListView.as_view(), name='control_asistencia'),  # Vista para el control de asistencia filtrado

    # Rutas relacionadas con los residentes
    path('residentes/', ResidentesListView.as_view(), name='residentes_list'),  # Vista para listar todos los residentes
    path('evaluacion_periodica/crear/', EvaluacionPeriodicaCreateView.as_view(), name='evaluacion_periodica_crear'),  # Vista para crear una evaluación periódica
    path('evaluacion_periodica/exito/', TemplateView.as_view(template_name='presentes/evaluacion_periodica_exito.html'), name='evaluacion_exitosa'),  # Vista para mostrar un mensaje de éxito al crear una evaluación periódica
    path('evaluados/', EvaluadosListView.as_view(), name='evaluados'),  # Vista para listar los residentes que han sido evaluados
    path('evaluados/<int:pk>/', EvaluadosDetailView.as_view(), name='evaluado_detail'),  # Vista para ver el detalle de un residente evaluado
    path('ateneo_evaluacion/crear/', AteneoEvaluacionCreateView.as_view(), name='ateneo_evaluacion_crear'),  # Vista para crear una evaluación del ateneo
    path('ateneo_evaluacion/', AteneoEvaluacionListView.as_view(), name='ateneo_evaluacion_list'),  # Vista para listar las evaluaciones del ateneo

    # Rutas relacionadas con clases y material de estudio
    path('clases_videos/', ClasesVideosListView.as_view(), name='clases_videos'),  # Vista para listar las clases

    # Rutas relacionadas con herramientas utiles para los residentes
    path('washout_suprarrenal/', CalcularWashoutView.as_view(), name='washout_suprarrenal'),  # Vista para calcular el washout suprarrenal

    # Rutas relacionadas con los perfiles de usuario
    path('perfil/', PerfilView.as_view(), name='perfil'),

    # Rutas relacionadas con las sedes
    path('sedes/nueva/', SedesCreateView.as_view(), name='sedes_create'),  # Vista para crear una nueva sede
    path('sedes/', SedesListView.as_view(), name='sedes_list'),  # Vista para listar todas las sedes
    path('sede/update/<int:pk>/', SedeUpdateView.as_view(), name='sede_update'),  # Vista para editar una sede
    path('sede/delete/<int:pk>/', SedeDeleteView.as_view(), name='sede_delete'),  # Vista para eliminar una sede

    # Rutas relacionadas con los códigos QR
    path('generar_qr/', views.generar_qr, name='generar_qr'),  # Vista para generar un código QR

    # Rutas relacionadas con los errores
    path('error_sin_perfil_residente/', TemplateView.as_view(template_name='presentes/error_sin_perfil_residente.html'), name='error_sin_perfil_residente'),  # Vista para el error cuando no existe un perfil de residente
]