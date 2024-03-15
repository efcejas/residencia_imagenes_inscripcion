from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pregunta_id>/", views.detalle, name="detalle"), # ejemplo: /encuestas/5/
    path("<int:pregunta_id>/resultados/", views.resultados, name="resultados"), # ejemplo: /encuestas/5/resultados/
    path("<int:pregunta_id>/votar/", views.votar, name="votar"), # ejemplo: /encuestas/5/votar/
]
