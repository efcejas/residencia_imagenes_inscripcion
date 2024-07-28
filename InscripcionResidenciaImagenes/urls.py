"""
URL configuration for InscripcionResidenciaImagenes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from asistencia.views import SuccessView, RegistroView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Rutas de la página principal
    path('', TemplateView.as_view(template_name='presentes/home.html'), name='home'),

    # Rutas de autenticación
    path('accounts/cerrar_sesion/', auth_views.LogoutView.as_view(template_name='registration/cerrar_sesion.html'), name='cerrar_sesion'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/<str:tipo_usuario>/', RegistroView.as_view(), name='register'),
    path('registro_exitoso/', SuccessView.as_view(), name='registro_exitoso'),

    # Rutas de selección de usuario
    path('seleccion_tipo_usuario/', TemplateView.as_view(template_name='registration/seleccion_tipo_usuario.html'), name='seleccion_tipo_usuario'),

    # Rutas de la aplicación 'asistencia'
    path('asistencia/', include(('asistencia.urls', 'asistencia'), namespace='asistencia')),

    # Rutas de la aplicación de la base de datos de casos interesantes
    path('casos_interesantes_db/', include(('casos_interesantes_db.urls', 'casos_interesantes_db'), namespace='casos_interesantes_db')),

    # Rutas de administración
    path('admin/', admin.site.urls),
]