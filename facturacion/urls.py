from django.urls import path
from .views import PacienteCreateView, HomePageView

app_name = "facturacion"

urlpatterns = [
    # Ruta para la vista de registro de pacientes
    path('', HomePageView.as_view(), name='inicio'),
    path('registro/', PacienteCreateView.as_view(), name='registro_pacientes'),
]
