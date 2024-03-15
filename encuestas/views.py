from django.shortcuts import render # Importamos la función `render` para utilizar un HTML
from django.http import HttpResponse, Http404 # Importamos la clase `HttpResponse` para generar una respuesta a la solicitud
from django.template import loader # Importamos `loader` para cargar plantillas
from django.shortcuts import render, get_object_or_404 # Importamos `get_object_or_404` para obtener un objeto o devolver un error 404
# Create your views here.

from .models import Pregunta

def index(request):
    ultima_pregunta_lista = Pregunta.objects.order_by("-fecha_publicacion")[:5]
    context = {
        "ultima_pregunta_lista": ultima_pregunta_lista
    }
    return render(request, "preguntas/index.html", context)

def detalle(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, "preguntas/detalle.html", {"pregunta": pregunta})

def resultados(request, pregunta_id):
    response = "Estás viendo los resultados de la pregunta %s."
    return HttpResponse(response % pregunta_id)

def votar(request, pregunta_id):
    return HttpResponse("Estás votando en la pregunta %s." % pregunta_id)
