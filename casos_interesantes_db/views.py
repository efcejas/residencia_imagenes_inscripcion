from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.views import View
from .models import CasoInteresante, ImagenCasoInteresante, Paciente
from .forms import CasoInteresanteForm, PacienteForm, ImagenCasoInteresanteForm

class CrearCasoInteresanteView(CreateView):
    model = CasoInteresante
    form_class = CasoInteresanteForm
    template_name = 'casos_db/crear_caso_interesante.html'
    success_url = reverse_lazy('casos_interesantes_db:crear_caso_interesante')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['paciente_form'] = PacienteForm(self.request.POST)
            data['imagen_form'] = ImagenCasoInteresanteForm(self.request.POST, self.request.FILES)
        else:
            data['paciente_form'] = PacienteForm()
            data['imagen_form'] = ImagenCasoInteresanteForm()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        paciente_form = context['paciente_form']
        imagen_form = context['imagen_form']

        if paciente_form.is_valid() and imagen_form.is_valid():
            dni = paciente_form.cleaned_data.get('dni')
            paciente, created = Paciente.objects.get_or_create(
                dni=dni,
                defaults={
                    'nombre': paciente_form.cleaned_data.get('nombre'),
                    'apellido': paciente_form.cleaned_data.get('apellido')
                }
            )

            # Si el paciente ya existe, actualizar sus datos
            if not created:
                paciente.nombre = paciente_form.cleaned_data.get('nombre')
                paciente.apellido = paciente_form.cleaned_data.get('apellido')
                paciente.save()

            # Asignar el paciente al caso interesante
            form.instance.paciente = paciente
            response = super().form_valid(form)

            # Guardar la imagen del caso interesante
            if imagen_form.cleaned_data.get('imagen'):
                imagen = ImagenCasoInteresante(caso=self.object, imagen=imagen_form.cleaned_data['imagen'])
                imagen.save()

            return response
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

class BuscarPacienteView(View):
    def get(self, request, *args, **kwargs):
        dni = request.GET.get('dni', None)
        if dni:
            try:
                paciente = Paciente.objects.get(dni=dni)
                data = {
                    'nombre': paciente.nombre,
                    'apellido': paciente.apellido,
                }
                return JsonResponse(data)
            except Paciente.DoesNotExist:
                return JsonResponse({'error': 'Paciente no encontrado'}, status=404)
        return JsonResponse({'error': 'DNI no proporcionado'}, status=400)