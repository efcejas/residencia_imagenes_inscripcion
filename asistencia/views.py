# Django imports
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat, TruncMonth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Librerías de terceros
import qrcode
from django.db.models import Q  # Para hacer consultas más complejas

# Local imports
from .forms import (RegistroAsistenciaForm, RegistroFormAdministrativo,
                    RegistroFormDocente, RegistroFormResidente, RegistroFormUsuario, SedeForm)
from .models import RegistroAsistencia, Residente, Usuario, Sedes

# Vistas relacionadas con el registro, login y logout de usuarios, además de la autenticación.abs


class RegistroView(CreateView):
    template_name = 'registration/register.html'
    # Redirige a la página de registro exitoso
    success_url = reverse_lazy('registro_exitoso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_usuario = self.kwargs.get('tipo_usuario')
        context['user_form'] = RegistroFormUsuario(self.request.POST or None)
        # Pasamos el tipo de usuario al contexto
        context['tipo_usuario'] = tipo_usuario
        return context

    def get_form_class(self):
        tipo_usuario = self.kwargs.get('tipo_usuario')
        if tipo_usuario == 'residente':
            return RegistroFormResidente
        elif tipo_usuario == 'docente':
            return RegistroFormDocente
        else:  # asumimos que el usuario es Administrativo
            return RegistroFormAdministrativo

    def form_valid(self, form):
        tipo_usuario = self.kwargs.get('tipo_usuario')
        context = self.get_context_data()
        user_form = context['user_form']
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        # El formulario no es válido, vuelve a renderizar la página de registro con el formulario y los errores de validación
        return self.render_to_response(self.get_context_data(form=form))


class SuccessView(TemplateView):
    template_name = 'registration/success.html'

# Vistas relacionadas con la página de asistencia.


class RegistroAsistenciaView(LoginRequiredMixin, View):
    def get(self, request):
        form = RegistroAsistenciaForm()
        return render(request, 'presentes/registro_asistencia.html', {'form': form})

    def post(self, request):
        # Verificar si el usuario tiene un perfil de residente asociado
        if hasattr(request.user, 'residente_profile'):
            # El usuario tiene un perfil de residente asociado
            form = RegistroAsistenciaForm(request.POST)
            if form.is_valid():
                ahora = timezone.localtime()

                residente = request.user.residente_profile
                ya_registrado_hoy = RegistroAsistencia.objects.filter(
                    residente=residente, fecha=ahora.date()).exists()

                if ya_registrado_hoy:
                    error_message = '¡{}, ya has registrado tu asistencia hoy!'.format(
                        request.user.first_name)
                    return render(request, 'presentes/registro_asistencia.html', {'form': form, 'error_message': error_message, 'error_url': reverse('asistencia:asistencias_registradas')})

                latitud = form.cleaned_data.get('latitud')
                longitud = form.cleaned_data.get('longitud')

                # Coordenadas de la sede pichincha de Investigaciones Médicas.
                latitud_permitida = -34.61068
                longitud_permitida = -58.39927
                rango_permitido = 0.0005
                if not (latitud_permitida - rango_permitido <= latitud <= latitud_permitida + rango_permitido and
                        longitud_permitida - rango_permitido <= longitud <= longitud_permitida + rango_permitido):
                    error_message = '¡{}, debes estar dentro del rango permitido para registrar tu asistencia!'.format(
                        request.user.first_name)
                    return render(request, 'presentes/registro_asistencia.html', {'form': form, 'error_message': error_message, 'error_url': reverse('asistencia:asistencias_registradas')})

                hora_inicio_entrada = ahora.replace(
                    hour=6, minute=30, second=0)
                hora_fin_entrada = ahora.replace(hour=7, minute=5, second=0)
                hora_inicio_clase = ahora.replace(hour=7, minute=0, second=0)
                hora_fin_clase = ahora.replace(hour=8, minute=0, second=0)

                if not (hora_inicio_entrada <= ahora <= hora_fin_entrada) and not (hora_inicio_clase <= ahora <= hora_fin_clase):
                    error_message = '¡{}, no es posible registrar asistencias fuera del horario permitido!'.format(
                        request.user.first_name)
                    return render(request, 'presentes/registro_asistencia.html', {'form': form, 'error_message': error_message, 'error_url': reverse('asistencia:asistencias_registradas')})

                if hora_fin_entrada < ahora <= hora_fin_clase:
                    llegada_tarde = True
                    llegada_a_tiempo = False
                else:
                    llegada_a_tiempo = hora_inicio_entrada <= ahora <= hora_fin_entrada
                    llegada_tarde = ahora > hora_fin_entrada

                registro_asistencia = form.save(commit=False)
                registro_asistencia.residente = residente
                registro_asistencia.fecha = ahora.date()
                registro_asistencia.hora = ahora.time()
                registro_asistencia.llegada_a_tiempo = llegada_a_tiempo
                registro_asistencia.llegada_tarde = llegada_tarde
                registro_asistencia.save()

                if llegada_tarde:
                    messages.error(request, '¡{}, registraste tu asistencia con tardanza!'.format(
                        request.user.first_name))
                else:
                    messages.success(request, '¡{}, registraste tu asistencia exitosamente!'.format(
                        request.user.first_name))

                return redirect('asistencia:asistencias_registradas')

            return render(request, 'presentes/registro_asistencia.html', {'form': form})

        # Si el usuario no tiene un perfil de residente asociado, maneja este caso según sea necesario
        else:
            error_message = 'Para poder marcar tu asistencia, necesitas tener un perfil de residente. Por favor, contacta al administrador para que te ayude a crear uno.'
            request.session['error_message'] = error_message
            return redirect('error_sin_perfil_residente')


class ListaAsistenciaView(LoginRequiredMixin, TemplateView):
    template_name = 'presentes/lista_asistencias_registradas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtiene el perfil asociado al usuario actual
        perfil_usuario = self.request.user.residente_profile
        # Obtiene todos los registros de asistencia del residente asociado
        context['attendance_records'] = RegistroAsistencia.objects.filter(
            residente=perfil_usuario).order_by('-fecha', '-hora')
        return context

# Vista para mostrar los registros de asistencia de un residente o de todos los residentes


class RegistroAsistenciaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = RegistroAsistencia
    template_name = 'presentes/lista_control_asistencia.html'
    context_object_name = 'control_asistencia'

    def get_queryset(self):
        return RegistroAsistencia.objects.annotate(
            mes=TruncMonth('fecha')
        ).order_by('-mes', '-fecha', '-hora')

    def test_func(self):
        return hasattr(self.request.user, 'docente_profile') or hasattr(self.request.user, 'administrativo_profile') or self.request.user.is_superuser

    def handle_no_permission(self):
        # redirige a la página de inicio o a una página de error si el usuario no tiene permiso
        return redirect('home')

# Vistas relacionadas con la gestión de usuarios residentes


class ResidentesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Residente
    template_name = 'presentes/residentes_list.html'
    context_object_name = 'residentes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_residentes'] = Residente.objects.count()
        return context

    def test_func(self):
        # Agregué perfil docente y superuser.
        return hasattr(self.request.user, 'administrativo_profile') or hasattr(self.request.user, 'docente_profile') or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('home')

# Vistas relacionadas con la gestion de sedes


class SedesCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Sedes
    form_class = SedeForm
    template_name = 'presentes/sede_form.html'
    success_url = reverse_lazy('asistencia:sedes_list')
    success_message = '¡La sede se ha creado exitosamente!'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.method == 'POST':
            return render(self.request, self.template_name, {'form': form})
        return response

    def test_func(self):
        return hasattr(self.request.user, 'administrativo_profile')

    def handle_no_permission(self):
        return redirect('home')


class SedesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Sedes
    template_name = 'presentes/sedes_list.html'
    context_object_name = 'sedes'

    def test_func(self):
        return hasattr(self.request.user, 'administrativo_profile') or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('home')

class SedeUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Sedes
    fields = ['nombre_sede', 'direccion', 'telefono', 'referente']
    template_name = 'presentes/sede_form.html'
    success_url = reverse_lazy('asistencia:sedes_list')
    success_message = '¡La sede se ha actualizado exitosamente!'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.method == 'POST':
            return render(self.request, self.template_name, {'form': form})
        return response

    def test_func(self):
        return hasattr(self.request.user, 'administrativo_profile')

    def handle_no_permission(self):
        return redirect('home')


class SedeDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Sedes
    template_name = 'presentes/sede_confirm_delete.html'
    success_url = reverse_lazy('asistencia:sedes_list')
    success_message = '¡La sede se ha eliminado exitosamente!'

    def test_func(self):
        return hasattr(self.request.user, 'administrativo_profile')

    def handle_no_permission(self):
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sede'] = self.object
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Create your views here.


def generar_qr(request):  # genera un qr con la url de la pagina de asistencia
    # se pone la url de la pagina de asistencia
    img = qrcode.make(
        'https://residentes-dm-9833103dde7d.herokuapp.com/asistencia/registro_asistencia/')
    img.save('qr.png')  # se guarda el qr en un archivo
    # se muestra un mensaje de que el qr fue generado
    return HttpResponse("QR generado.")
