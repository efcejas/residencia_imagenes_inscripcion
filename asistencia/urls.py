from django.urls import path
from .views import RegistroAsistenciaView, ListaAsistenciaView, HomeView

from . import views

app_name = "asistencia"
urlpatterns = [
    path('generar_qr/', views.generar_qr, name='generar_qr'),
    path('registro_asistencia/', RegistroAsistenciaView.as_view(), name='registro_asistencia'),
    path('asistencias_registradas/', ListaAsistenciaView.as_view(), name='asistencias_registradas'),
]