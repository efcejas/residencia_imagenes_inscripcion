# Django imports
from django.shortcuts import render  # Usado para renderizar plantillas
from django.http import HttpResponse  # Usado para devolver respuestas HTTP
from django.core.files.base import ContentFile  # Usado para manejar archivos
from django.views.generic import TemplateView  # Usado para crear vistas basadas en clases


# Librerías de terceros
import datetime  # Usado para manejar fechas y horas
import qrcode  # Usado para generar códigos QR
from PIL import Image  # Usado para manejar imágenes

class InicioView(TemplateView):
    template_name = "presentes/inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega aquí cualquier dato adicional que necesites en la plantilla.
        current_year = datetime.datetime.now().year
        # Agrega el año actual al contexto
        context["year"] = current_year
        return context


def prueba(request):
    return HttpResponse("Hola, mundo.")

# Create your views here.

def generar_qr(request): #genera un qr con la url de la pagina de asistencia
    img = qrcode.make('http://192.168.0.71:8000/asistencia/prueba/') #se pone la url de la pagina de asistencia
    img.save('qr.png') #se guarda el qr en un archivo   
    return HttpResponse("QR generado.") #se muestra un mensaje de que el qr fue generado

