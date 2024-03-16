from django.urls import path

from . import views

app_name = "encuestas"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"), # ejemplo: /encuestas/
    path("<int:pk>/", views.DetalleView.as_view(), name="detalle"), # ejemplo: /encuestas/5/
    path("<int:pk>/resultados/", views.ResultadosView.as_view(), name="resultados"), # ejemplo: /encuestas/5/resultados/
    path("<int:pregunta_id>/votar/", views.votar, name="votar"), # ejemplo: /encuestas/5/votar/
]
