from django.urls import path
from django.views.generic import TemplateView
from .views import (
    PacienteSearchView,
    PacienteCreateView,
    CasoInteresanteCreateView,
    CasoCreadoExitoView,
    CasoInteresanteListView,
    CasoInteresanteDetailView
)

app_name = "casos_interesantes_db"

urlpatterns = [
    path('en_construccion/', TemplateView.as_view(
        template_name='casos_db/pagina_en_construccion.html'), name='en_construccion'),
    path('buscar_paciente/', PacienteSearchView.as_view(), name='buscar_paciente'),
    path('crear_paciente/', PacienteCreateView.as_view(), name='crear_paciente'),
    path('crear_caso_interesante/<int:paciente_id>/', CasoInteresanteCreateView.as_view(), name='crear_caso_interesante'),
    path('caso-creado-exito/<int:pk>/', CasoCreadoExitoView.as_view(), name='caso_creado_exito'),
    path('casos/', CasoInteresanteListView.as_view(), name='lista_casos_interesantes'),
    path('casos/<int:pk>/', CasoInteresanteDetailView.as_view(), name='detalle_caso_interesante'),
]