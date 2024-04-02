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
from asistencia.views import RegisterResidenteView, CustomLogoutView, SuccessView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('encuestas/', include('encuestas.urls')), # Agregamos la ruta de la aplicación 'encuestas'
    path('asistencia/', include(('asistencia.urls', 'asistencia'), namespace='asistencia')), # Agregamos la ruta de la aplicación 'asistencia' (se pone ('asistencia.urls', 'asistencia') para que sepa que es una aplicacion y cumpla con el estandar de Django
    # Urls para el manejo de autenticación
    path('register/', RegisterResidenteView.as_view(), name='register'),
    path('registro_exitoso/', SuccessView.as_view(), name='registro_exitoso'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]
