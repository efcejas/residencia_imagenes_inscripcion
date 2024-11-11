# imat/urls.py
from django.urls import path
from . import views
from .views import InicioImatView, BienvenidaView, DatosPersonalesView, ExamenView, ExamenCompletadoView, ResidentesExamenListView, ResidenteExamenDetailView

app_name = 'imat'  # Definir el namespace

urlpatterns = [
    path('', InicioImatView.as_view(), name='home_imat'),
    path('bienvenida/', BienvenidaView.as_view(), name='bienvenida'),
    path('datos-personales/', DatosPersonalesView.as_view(), name='datos_personales'),
    path('examen/', ExamenView.as_view(), name='examen'),
    path('examen-completado/', ExamenCompletadoView.as_view(), name='examen_completado'),
    path('salir/', views.salir, name='salir'),
    path('residentes-examen/', ResidentesExamenListView.as_view(), name='residentes_examen'),
    path('residente-examen/<int:pk>/', ResidenteExamenDetailView.as_view(), name='residente_examen_detail'),
]
