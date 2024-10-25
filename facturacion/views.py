from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, ListView
from django.http import HttpResponse, JsonResponse

from .models import Paciente, PacienteRegion, Empresa
from .forms import PacienteForm, PacienteRegionForm, EmpresaForm

class HomePageView(TemplateView):
    template_name = 'facturacion/drcejasinicio.html'

# Selección de empresa
def seleccionar_empresa(request):
    if request.method == 'POST':
        empresa_id = request.POST.get('empresa')
        request.session['empresa_id'] = empresa_id  # Guardamos la empresa en la sesión
        messages.success(request, 'Empresa seleccionada exitosamente.')
        return redirect('facturacion:registro_pacientes')

    empresas = Empresa.objects.all()
    return render(request, 'facturacion/seleccionar_empresa.html', {'empresas': empresas})

# Vista de creación de pacientes, con la lógica de empresa y cantidad de regiones

# Registro de Pacientes
class PacienteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'facturacion/registro_pacientes.html'
    success_url = reverse_lazy('facturacion:registro_pacientes')

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa_id = self.request.session.get('empresa_id')
        if empresa_id:
            context['empresa'] = get_object_or_404(Empresa, id=empresa_id)
        context['region_form'] = PacienteRegionForm()
        today = datetime.now().date()
        context['pacientes_registrados'] = PacienteRegion.objects.filter(
            empresa_id=empresa_id, fecha__date=today
        )
        return context

    def form_valid(self, form):
        empresa_id = self.request.session.get('empresa_id')
        empresa = get_object_or_404(Empresa, id=empresa_id)

        # Crear o buscar el paciente
        dni = form.cleaned_data.get('dni')
        paciente, created = Paciente.objects.get_or_create(
            dni=dni,
            defaults={'nombre': form.cleaned_data['nombre'], 'apellido': form.cleaned_data['apellido']}
        )

        # Registrar las regiones
        region_form = PacienteRegionForm(self.request.POST)
        if region_form.is_valid():
            paciente_region = PacienteRegion.objects.create(
                paciente=paciente,
                empresa=empresa,
                fecha=region_form.cleaned_data['fecha']
            )
            paciente_region.regiones.set(region_form.cleaned_data['regiones'])
            paciente_region.save()

            messages.success(self.request, 'Paciente registrado exitosamente.' if created else 'Nueva atención registrada.')

        return redirect(self.success_url)