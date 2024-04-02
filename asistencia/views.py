# Django imports
from django.shortcuts import render, redirect  # Usado para renderizar plantillas
from django.http import HttpResponse  # Usado para devolver respuestas HTTP
from django.core.files.base import ContentFile  # Usado para manejar archivos
from django.contrib.auth.decorators import login_required  # Decorador para requerir autenticación
from django.views.generic import TemplateView  # Usado para crear vistas basadas en clases
from django.views.generic.edit import CreateView, FormView  # Usado para crear vistas basadas en clases
from django.urls import reverse_lazy  # Usado para redirigir a una URL después de realizar una acción
from django.contrib.auth.views import LogoutView  # Importa la vista de logout de Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from .models import Residente, RegistroAsistencia  # Importa los modelos de Residente y RegistroAsistencia
from .forms import ResidenteRegistrationForm, RegistroAsistenciaForm # Importa el formulario de registro de residentes


# Librerías de terceros
import datetime  # Usado para manejar fechas y horas
import qrcode  # Usado para generar códigos QR
from PIL import Image  # Usado para manejar imágenes

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

# Vistas relacionadas con la página de inicio de la aplicación.

class InicioView(LoginRequiredMixin, TemplateView):
    template_name = "presentes/inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega aquí cualquier dato adicional que necesites en la plantilla.
        current_year = datetime.datetime.now().year
        # Agrega el año actual al contexto
        context["year"] = current_year
        return context

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
            registro_asistencia.save()
            return redirect('asistencia:inicio')
        print(form.errors)  # Imprime los errores del formulario
        return render(request, 'presentes/registro_asistencia.html', {'form': form})

# Otras vistas de prueba

def prueba(request):
    return HttpResponse("Hola, mundo.")

# Create your views here.

def generar_qr(request): #genera un qr con la url de la pagina de asistencia
    img = qrcode.make('http://192.168.0.71:8000/asistencia/registrar_asistencia/') #se pone la url de la pagina de asistencia
    img.save('qr.png') #se guarda el qr en un archivo   
    return HttpResponse("QR generado.") #se muestra un mensaje de que el qr fue generado

