from django.urls import path
from .views import HomePageView, seleccionar_empresa, PacienteCreateView

urlpatterns = [
    path('', HomePageView.as_view(), name='inicio'),
    path('seleccionar_empresa/', seleccionar_empresa, name='seleccionar_empresa'),
    path('registro_pacientes/', PacienteCreateView.as_view(), name='registro_pacientes'),
    # Otras rutas...
]