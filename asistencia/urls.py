from django.urls import path

from . import views

app_name = "asistencia"
urlpatterns = [
    path('prueba/', views.prueba, name='prueba'),
    path('generar_qr/', views.generar_qr, name='generar_qr'), # debe ponerse asistencia/generar_qr/ para que sepa que es de la aplicacion asistencia
]