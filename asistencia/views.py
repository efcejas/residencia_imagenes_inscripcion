# Django imports
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views import View
from .models import Residente, RegistroAsistencia, Usuario
from .forms import RegistroAsistenciaForm

# Librerías de terceros
from django.utils import timezone
from django.db.models import Q # Para hacer consultas más complejas
import qrcode

# Vistas relacionadas con el registro, login y logout de usuarios, además de la autenticación.abs

""" class RegisterResidenteView(SuccessMessageMixin, CreateView):
    form_class = ResidenteRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('registro_exitoso')  # reemplaza 'login' con la URL a la que quieres redirigir
    success_message = "Gracias por registrarte, %(username)s! Ahora puedes iniciar sesión."

    def get_success_message(self, cleaned_data):
        # Aquí, reemplazamos %(username)s en success_message con el nombre de usuario del objeto recién creado
        return self.success_message % dict(cleaned_data, username=self.object.username) """

class SuccessView(TemplateView):
    template_name = 'registration/success.html'

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

# Vistas relacionadas con la página de asistencia.

class HomeView(TemplateView):
    template_name = 'presentes/home.html'

class RegistroAsistenciaView(LoginRequiredMixin, View):
    def get(self, request):
        form = RegistroAsistenciaForm()
        return render(request, 'presentes/registro_asistencia.html', {'form': form})

    def post(self, request):
        form = RegistroAsistenciaForm(request.POST)
        if form.is_valid():
            ahora = timezone.localtime()

            ya_registrado_hoy = RegistroAsistencia.objects.filter(residente=request.user, fecha=ahora.date()).exists()
            if ya_registrado_hoy:
                error_message = '¡{}, ya has registrado tu asistencia hoy!'.format(request.user.first_name)
                return render(request, 'presentes/registro_asistencia.html', {'form': form, 'error_message': error_message, 'error_url': reverse('asistencia:asistencias_registradas')})

            latitud = form.cleaned_data.get('latitud')
            longitud = form.cleaned_data.get('longitud')

            latitud_permitida = -34.61073
            longitud_permitida = -58.39922
            rango_permitido = 0.0005
            if not (latitud_permitida - rango_permitido <= latitud <= latitud_permitida + rango_permitido and
                    longitud_permitida - rango_permitido <= longitud <= longitud_permitida + rango_permitido):
                error_message = '¡{}, debes estar dentro del rango permitido para registrar tu asistencia!'.format(request.user.first_name)
                return render(request, 'presentes/registro_asistencia.html', {'form': form, 'error_message': error_message, 'error_url': reverse('asistencia:asistencias_registradas')})

            hora_inicio_entrada = ahora.replace(hour=6, minute=30, second=0)
            hora_fin_entrada = ahora.replace(hour=7, minute=5, second=0)
            hora_inicio_clase = ahora.replace(hour=7, minute=0, second=0)
            hora_fin_clase = ahora.replace(hour=8, minute=0, second=0)

            if not (hora_inicio_entrada <= ahora <= hora_fin_entrada) and not (hora_inicio_clase <= ahora <= hora_fin_clase):
                error_message = '¡{}, no es posible registrar asistencias fuera del horario permitido!'.format(request.user.first_name)
                return render(request, 'presentes/registro_asistencia.html', {'form': form, 'error_message': error_message, 'error_url': reverse('asistencia:asistencias_registradas')})

            if hora_fin_entrada < ahora <= hora_fin_clase:
                llegada_tarde = True
                llegada_a_tiempo = False
            else:
                llegada_a_tiempo = hora_inicio_entrada <= ahora <= hora_fin_entrada
                llegada_tarde = ahora > hora_fin_entrada

            registro_asistencia = form.save(commit=False)
            registro_asistencia.residente = request.user
            registro_asistencia.fecha = ahora.date()
            registro_asistencia.hora = ahora.time()
            registro_asistencia.llegada_a_tiempo = llegada_a_tiempo
            registro_asistencia.llegada_tarde = llegada_tarde
            registro_asistencia.save()

            if llegada_tarde:
                messages.error(request, '¡{}, registraste tu asistencia con tardanza!'.format(request.user.first_name))
            else:
                messages.success(request, '¡{}, registraste tu asistencia exitosamente!'.format(request.user.first_name))

            return redirect('asistencia:asistencias_registradas')

        return render(request, 'presentes/registro_asistencia.html', {'form': form})

class ListaAsistenciaView(LoginRequiredMixin, TemplateView):
    template_name = 'presentes/lista_asistencias_registradas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtiene todos los registros de asistencia del usuario actual
        context['attendance_records'] = RegistroAsistencia.objects.filter(residente=self.request.user).order_by('-fecha', '-hora')
        return context

# Create your views here.

def generar_qr(request): #genera un qr con la url de la pagina de asistencia
    img = qrcode.make('https://residentes-dm-9833103dde7d.herokuapp.com/asistencia/registro_asistencia/') #se pone la url de la pagina de asistencia
    img.save('qr.png') #se guarda el qr en un archivo   
    return HttpResponse("QR generado.") #se muestra un mensaje de que el qr fue generado

