from django.shortcuts import render # Importamos la función `render` para utilizar un HTML
from django.http import HttpResponse, Http404, HttpResponseRedirect # Importamos la clase `HttpResponse` para generar una respuesta a la solicitud
from django.template import loader # Importamos `loader` para cargar plantillas
from django.shortcuts import render, get_object_or_404 # Esto sirve para mostrar un error 404 si el objeto no existe
from django.urls import reverse # Esto sirve para redirigir a una vista específica
from django.db.models import F # Esto sirve para evitar problemas de concurrencia
from django.views import generic # Esto sirve para crear vistas genéricas
from django.utils import timezone # Esto sirve para manejar la zona horaria

from .models import Pregunta, Opcion

class IndexView(generic.ListView):
    template_name = "preguntas/index.html"
    context_object_name = "ultima_pregunta_lista"

    def get_queryset(self):
        """Devuelve las últimas cinco preguntas publicadas."""
        return Pregunta.objects.filter(
            fecha_publicacion__lte=timezone.now()
        ).order_by("-fecha_publicacion")[:5]

class DetalleView(generic.DetailView):
    model = Pregunta
    template_name = "preguntas/detalle.html"

    def get_queryset(self):
        """
        Excluye cualquier pregunta que no haya sido publicada todavía.
        """
        return Pregunta.objects.filter(fecha_publicacion__lte=timezone.now())

class ResultadosView(generic.DetailView):
    model = Pregunta
    template_name = "preguntas/resultados.html"

def votar(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        opcion_seleccionada = pregunta.opcion_set.get(pk=request.POST["opcion"])
    except (KeyError, Opcion.DoesNotExist):
        # Vuelva a mostrar el formulario de votación de preguntas.
        return render(request, "preguntas/detalle.html", {
            "pregunta": pregunta,
            "error_message": "No seleccionaste una opción."
        },)
    else:
        opcion_seleccionada.votos = F("votos") + 1
        opcion_seleccionada.save()
        # Siempre devolver un HttpResponseRedirect después de realizar una transacción exitosa 
        # con datos POST. Esto evita que los datos se publiquen dos veces si 
        # usuario presiona el botón Atrás.
        return HttpResponseRedirect(reverse("encuestas:resultados", args=(pregunta.id,)))
