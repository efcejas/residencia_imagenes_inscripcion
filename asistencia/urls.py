from django.urls import path
from django.views.generic import TemplateView
from .views import RegistroAsistenciaView, ListaAsistenciaView, RegistroAsistenciaListView, SedesCreateView, SedesListView, SedeUpdateView, SedeDeleteView, ResidentesListView, CalcularWashoutView

from . import views

app_name = "asistencia"
urlpatterns = [
    # Rutas relacionadas con la asistencia
    path('registro_asistencia/', RegistroAsistenciaView.as_view(), name='registro_asistencia'),  # Vista para registrar la asistencia
    path('asistencias_registradas/', ListaAsistenciaView.as_view(), name='asistencias_registradas'),  # Vista para listar las asistencias registradas
    path('control_asistencia/', RegistroAsistenciaListView.as_view(), name='control_asistencia'),  # Vista para el control de asistencia

    # Rutas relacionadas con los residentes
    path('residentes/', ResidentesListView.as_view(), name='residentes_list'),  # Vista para listar todos los residentes

    # Rutas relacionadas con herramientas utiles para los residentes
    path('washout_suprarrenal/', CalcularWashoutView.as_view(), name='washout_suprarrenal'),  # Vista para calcular el washout suprarrenal

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