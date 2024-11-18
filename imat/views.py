from django import forms
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, FormView, ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView
from .forms import DatosPersonalesForm, ExamenForm
from .models import Residente, Examen, ExamenRespuesta, EvaluacionPractica
from asistencia.models import Usuario
from imat.forms import RegistroImatForm, ExamenRespuestaForm, EvaluacionPracticaForm

# Vista de registro de usuario para Imat
class RegistroImatView(CreateView):
    model = Usuario
    form_class = RegistroImatForm
    template_name = 'registration-imat/register.html'
    success_url = reverse_lazy('register_success_imat')

class RegistroExitosoImatView(TemplateView):
    template_name = 'registration-imat/register_success.html'

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
        
        # Guardar el residente en la sesión
        self.request.session['residente_id'] = residente.id
        self.request.session['examen_id'] = Examen.objects.first().id

        # Redirigir directamente al examen si el residente ya existe
        if not creado:
            return redirect(self.success_url)

        return super().form_valid(form)

    def form_invalid(self, form):
        # Esto asegura que no se mostrará un mensaje de error si el residente ya existe
        dni = form.data.get('dni')
        if dni and Residente.objects.filter(dni=dni).exists():
            residente = Residente.objects.get(dni=dni)
            self.request.session['residente_id'] = residente.id
            self.request.session['examen_id'] = Examen.objects.first().id
            return redirect(self.success_url)
        return super().form_invalid(form)

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
        context['descripcion_examen'] = examen.descripcion
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

class ResidentesExamenListView(ListView):
    model = Residente
    template_name = 'imat/residentes_examen_list.html'
    context_object_name = 'residentes'

    def get_queryset(self):
        # Obtener el último examen presentado
        ultimo_examen_respuesta = ExamenRespuesta.objects.order_by('-fecha_realizacion').first()
        
        if ultimo_examen_respuesta:
            # Filtrar residentes que completaron el último examen
            return Residente.objects.filter(examenes_respuestas__examen=ultimo_examen_respuesta.examen).distinct()
        
        # Si no hay exámenes presentados, devolver un queryset vacío
        return Residente.objects.none()

class ResidenteExamenDetailView(DetailView):
    model = Residente
    template_name = 'imat/residente_examen_detail.html'
    context_object_name = 'residente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el último examen respondido por el residente
        examen_respuesta = ExamenRespuesta.objects.filter(residente=self.object).order_by('-fecha_realizacion').first()
        if examen_respuesta:
            context['examen_respuesta'] = examen_respuesta
            context['preguntas_respuestas'] = examen_respuesta.respuestas.all()

            # Incluir el formulario de calificación del examen
            context['form'] = ExamenRespuestaForm(instance=examen_respuesta)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Obtener el residente actual
        examen_respuesta_id = request.POST.get('examen_respuesta_id')
        examen_respuesta = ExamenRespuesta.objects.get(id=examen_respuesta_id)

        form = ExamenRespuestaForm(request.POST, instance=examen_respuesta)
        if form.is_valid():
            form.save()  # Guardar la calificación
            return redirect(reverse('imat:residente_examen_detail', args=[self.object.pk]))

        # Si el formulario no es válido, volver a cargar con errores
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
