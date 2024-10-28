from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .forms import DatosPersonalesForm, ExamenForm
from .models import Residente, Examen, ExamenRespuesta

# Vista de inicio para Imat
class InicioImatView(TemplateView):
    def get_template_names(self):
        if settings.SITE_ID == 2:
            print("Cargando template de Imat: inicioimat.html")
            return ['imat/inicioimat.html']
        print("Cargando template principal: home.html")
        return ['presentes/home.html']

# Vista de bienvenida
class BienvenidaView(TemplateView):
    template_name = 'imat/bienvenida.html'  # Mostrar mensaje de bienvenida y botón "Comenzar Examen"

# Vista para capturar datos personales del residente
class DatosPersonalesView(FormView):
    template_name = 'imat/datos_personales.html'
    form_class = DatosPersonalesForm
    success_url = reverse_lazy('imat:examen')

    def form_valid(self, form):
        dni = form.cleaned_data['dni']
        nombre = form.cleaned_data['nombre']
        apellido = form.cleaned_data['apellido']
        
        # Obtener o crear el residente
        residente, creado = Residente.objects.get_or_create(
            dni=dni,
            defaults={'nombre': nombre, 'apellido': apellido}
        )
        
        # Establecer el ID del residente y del examen en la sesión
        self.request.session['residente_id'] = residente.id
        self.request.session['examen_id'] = Examen.objects.first().id  # Selecciona un examen específico, o define cuál será el examen actual

        return super().form_valid(form)

# Vista para capturar respuestas del examen
class ExamenView(FormView):
    template_name = 'imat/examen.html'
    form_class = ExamenForm
    success_url = '/examen-completado/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtiene el examen usando el examen_id de la sesión
        examen_id = self.request.session.get('examen_id')
        examen = get_object_or_404(Examen, id=examen_id)
        
        # Pasar el título del examen al contexto
        context['titulo_examen'] = examen.titulo
        return context

    def form_valid(self, form):
        residente_id = self.request.session.get('residente_id')
        examen_id = self.request.session.get('examen_id')
        
        if residente_id and examen_id:
            residente = get_object_or_404(Residente, id=residente_id)
            examen = get_object_or_404(Examen, id=examen_id)
            
            # Crear intento de examen
            examen_respuesta = ExamenRespuesta.objects.create(
                residente=residente,
                examen=examen
            )
            
            # Guardar respuestas
            form.save(examen_respuesta=examen_respuesta)
            self.request.session['residente_nombre'] = f"{residente.nombre} {residente.apellido}"
        
        return super().form_valid(form)

# Vista de confirmación de examen completado
import logging
logger = logging.getLogger(__name__)

class ExamenCompletadoView(TemplateView):
    template_name = 'imat/examen_completado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['residente_nombre'] = self.request.session.get('residente_nombre', "Residente")
        
        # Log para verificar el contenido de residente_nombre
        logger.info(f"Nombre del residente en sesión: {context['residente_nombre']}")
        
        return context

def salir(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('imat:bienvenida') # Redirige a la vista de bienvenida
