# Django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views import View
from .models import Residente, RegistroAsistencia
from .forms import ResidenteRegistrationForm, RegistroAsistenciaForm

# Librerías de terceros
from django.utils import timezone
from django.db.models import Q # Para hacer consultas más complejas
import qrcode

# Vistas relacionadas con el registro, login y logout de usuarios, además de la autenticación.abs

class RegisterResidenteView(SuccessMessageMixin, CreateView):
    form_class = ResidenteRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('registro_exitoso')  # reemplaza 'login' con la URL a la que quieres redirigir
    success_message = "Gracias por registrarte, %(username)s! Ahora puedes iniciar sesión."

    def get_success_message(self, cleaned_data):
        # Aquí, reemplazamos %(username)s en success_message con el nombre de usuario del objeto recién creado
        return self.success_message % dict(cleaned_data, username=self.object.username)

class SuccessView(TemplateView):
    template_name = 'registration/success.html'

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

# Vistas relacionadas con la página de asistencia.

class RegistroAsistenciaView(LoginRequiredMixin, View):
    def get(self, request):
        form = RegistroAsistenciaForm()
        return render(request, 'presentes/registro_asistencia.html', {'form': form})

    def post(self, request):
        form = RegistroAsistenciaForm(request.POST)
        if form.is_valid():
            # Obtiene la hora actual
            
            ahora = timezone.now()
            ahora_local = timezone.localtime(ahora)
            print("Hora actual en zona horaria local:", ahora_local)

            # Verifica si el usuario ya ha registrado su asistencia hoy
            ya_registrado_hoy = RegistroAsistencia.objects.filter(residente=request.user, fecha_hora__date=ahora.date()).exists()
            # Imprime los datos para depuración
            print("Registro de asistencia:", ya_registrado_hoy)
            
            if ya_registrado_hoy:
                messages.error(request, '¡{}, ya has registrado tu asistencia hoy!'.format(request.user.first_name))
                return render(request, 'presentes/registro_asistencia.html', {'form': form})

            # Obtiene la ubicación del usuario
            latitud = form.cleaned_data.get('latitud')
            longitud = form.cleaned_data.get('longitud')

            # Verifica si la ubicación del usuario está dentro del rango permitido
            latitud_permitida = -34.60342544726747  # reemplaza con la latitud de tu ubicación
            longitud_permitida = -58.41512964682172  # reemplaza con la longitud de tu ubicación
            rango_permitido = 0.30  # reemplaza con el rango permitido en grados decimales
            if not (latitud_permitida - rango_permitido <= latitud <= latitud_permitida + rango_permitido and
                    longitud_permitida - rango_permitido <= longitud <= longitud_permitida + rango_permitido):
                messages.error(request, '¡{}, debes estar dentro del rango permitido para registrar tu asistencia!'.format(request.user.first_name))
                return render(request, 'presentes/registro_asistencia.html', {'form': form})

            # Verifica si la hora actual está dentro del rango permitido
            hora_inicio = ahora.replace(hour=18, minute=0, second=0)  # Cambiado a 18:00
            hora_fin = ahora.replace(hour=18, minute=45, second=0)  # Cambiado a 18:45
            
            # Si todas las verificaciones pasan, registra la asistencia
            llegada_a_tiempo = hora_inicio <= ahora < hora_fin
            llegada_tarde = ahora >= hora_fin
            registro_asistencia = form.save(commit=False)
            registro_asistencia.residente = request.user
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
        context['attendance_records'] = RegistroAsistencia.objects.filter(residente=self.request.user).order_by('-fecha_hora')
        return context

# Create your views here.

def generar_qr(request): #genera un qr con la url de la pagina de asistencia
    img = qrcode.make('http://127.0.0.1:8000/asistencia/registro_asistencia/') #se pone la url de la pagina de asistencia
    img.save('qr.png') #se guarda el qr en un archivo   
    return HttpResponse("QR generado.") #se muestra un mensaje de que el qr fue generado

