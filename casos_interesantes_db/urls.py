from django.urls import path # Importa la función path de django.urls
from django.views.generic import TemplateView # Importa la clase TemplateView de django.views.generic
from . import views # Importa las vistas definidas en el archivo views.py de la aplicación

app_name = "casos_interesantes_db"
urlpatterns = [
    path('en_construccion/', TemplateView.as_view(template_name='casos_db/pagina_en_construccion.html'), name='en_construccion'),
]