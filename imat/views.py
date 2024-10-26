# imat/views.py
from django.conf import settings
from django.views.generic import TemplateView

class InicioImatView(TemplateView):
    def get_template_names(self):
        if settings.SITE_ID == 2:
            print("Cargando template de Imat: inicioimat.html")
            return ['imat/inicioimat.html']
        print("Cargando template principal: home.html")
        return ['presentes/home.html']
