from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import CreateView

from .models import Paciente, PacienteRegion
from .forms import PacienteForm, PacienteRegionForm

class PacienteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'registro_pacientes.html'
    success_url = reverse_lazy('lista_pacientes')

    def test_func(self):
        # Solo permite acceso si el usuario es superusuario
        return self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirige al login si no tiene permiso
        return redirect('login')  # Ajusta esta URL según tu configuración de login

    def form_valid(self, form):
        dni = form.cleaned_data.get('dni')
        paciente, created = Paciente.objects.get_or_create(dni=dni, defaults={
            'nombre': form.cleaned_data.get('nombre'),
            'apellido': form.cleaned_data.get('apellido')
        })

        # Crear el registro de PacienteRegion
        region_form = PacienteRegionForm(self.request.POST)
        if region_form.is_valid():
            region_form.instance.paciente = paciente
            region_form.save()
        return super().form_valid(form)
