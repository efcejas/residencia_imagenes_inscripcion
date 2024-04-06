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
            registro_asistencia = form.save(commit=False)
            registro_asistencia.residente = request.user
            registro_asistencia.llegada_tarde = registro_asistencia.llego_tarde()
            registro_asistencia.save()

            if registro_asistencia.llegada_tarde:
                messages.error(request, '¡{}, registraste tu asistencia con tardanza!'.format(request.user.first_name))
            else:
                messages.success(request, '¡{}, registraste tu asistencia exitosamente!'.format(request.user.first_name))

            return redirect('asistencia:asistencias_registradas')
        return render(request, 'presentes/registro_asistencia.html', {'form': form})

class ListaAsistenciaView(LoginRequiredMixin, TemplateView):
    template_name = 'presentes/lista_asistencias_registradas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtiene los últimos registros de asistencia del usuario actual
        context['attendance_records'] = RegistroAsistencia.objects.filter(residente=self.request.user).order_by('-fecha_hora')[:6]
        return context

# Create your views here.

def generar_qr(request): #genera un qr con la url de la pagina de asistencia
    img = qrcode.make('http://127.0.0.1:8000/asistencia/registro_asistencia/') #se pone la url de la pagina de asistencia
    img.save('qr.png') #se guarda el qr en un archivo   
    return HttpResponse("QR generado.") #se muestra un mensaje de que el qr fue generado

