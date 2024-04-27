from django.urls import path
from django.views.generic import TemplateView
from .views import RegistroAsistenciaView, ListaAsistenciaView, RegistroAsistenciaListView

from . import views

app_name = "asistencia"
urlpatterns = [
    path('generar_qr/', views.generar_qr, name='generar_qr'),
    path('registro_asistencia/', RegistroAsistenciaView.as_view(), name='registro_asistencia'),
    path('error_sin_perfil_residente/', TemplateView.as_view(template_name='presentes/error_sin_perfil_residente.html'), name='error_sin_perfil_residente'),
    path('asistencias_registradas/', ListaAsistenciaView.as_view(), name='asistencias_registradas'),
    path('control_asistencia/', RegistroAsistenciaListView.as_view(), name='control_asistencia'),
]