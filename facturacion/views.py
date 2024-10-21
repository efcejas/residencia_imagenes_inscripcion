from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import CreateView, TemplateView

from .models import Paciente, PacienteRegion, Empresa
from .forms import PacienteForm, PacienteRegionForm
from datetime import datetime

class HomePageView(TemplateView):
    template_name = 'facturacion/drcejasinicio.html'

# Vista para seleccionar empresa al inicio de la jornada
def seleccionar_empresa(request):
    if request.method == 'POST':
        empresa_id = request.POST.get('empresa')
        request.session['empresa_id'] = empresa_id  # Guardar la empresa en la sesión
        return redirect('facturacion:registro_pacientes')  # Redirigir a la vista de registro de pacientes

    empresas = Empresa.objects.all()
    return render(request, 'facturacion/seleccionar_empresa.html', {'empresas': empresas})

# Vista de creación de pacientes, con la lógica de empresa y cantidad de regiones
class PacienteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'facturacion/registro_pacientes.html'
    success_url = reverse_lazy('facturacion:registro_pacientes')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        # Obtener la empresa seleccionada de la sesión
        empresa_id = self.request.session.get('empresa_id')
        if not empresa_id:
            messages.error(self.request, 'Debes seleccionar una empresa antes de registrar pacientes.')
            return redirect('facturacion:seleccionar_empresa')

        empresa = Empresa.objects.get(id=empresa_id)  # Obtener la empresa seleccionada
        dni = form.cleaned_data.get('dni')
        
        # Crear o recuperar al paciente
        paciente, created = Paciente.objects.get_or_create(
            dni=dni,
            defaults={
                'nombre': form.cleaned_data.get('nombre'),
                'apellido': form.cleaned_data.get('apellido')
            }
        )

        # Manejar las regiones y la cantidad de veces que se registran
        region_form = PacienteRegionForm(self.request.POST)
        if region_form.is_valid():
            region_form.instance.paciente = paciente
            region_form.instance.empresa = empresa
            region_form.instance.cantidad = region_form.cleaned_data.get('cantidad')  # Contabilizar la cantidad de regiones
            region_form.save()

        if created:
            messages.success(self.request, 'Paciente registrado exitosamente.')
        else:
            messages.success(self.request, 'Nueva atención registrada para el paciente.')

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        # Obtener los pacientes registrados hoy
        today = datetime.now().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        context = super().get_context_data(**kwargs)
        context['region_form'] = PacienteRegionForm()
        context['pacientes_registrados'] = PacienteRegion.objects.filter(fecha__range=(start_of_day, end_of_day))
        return context
