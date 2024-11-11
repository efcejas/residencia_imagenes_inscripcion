"""
Configuración de URL para el proyecto InscripcionResidenciaImagenes.

La lista `urlpatterns` dirige las URL a las vistas. Para obtener más información, consulte:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Ejemplos:
Vistas de funciones
    1. Agregue una importación: desde las vistas de importación de my_app
    2. Agregue una URL a urlpatterns: ruta('', views.home, nombre='home')
Vistas basadas en clases
    1. Agregue una importación: desde other_app.views import Inicio
    2. Agregue una URL a urlpatterns: ruta('', Home.as_view(), nombre='home')
Incluyendo otra URLconf
    1. Importe la función include(): desde django.urls importe include, ruta
    2. Agregue una URL a urlpatterns: ruta('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from asistencia.views import SuccessView, RegistroView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

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

    # Rutas de la aplicación de facturación
    path('facturacion/', include(('facturacion.urls', 'facturacion'), namespace='facturacion')),

    # Prefijo específico para Imat con su propio archivo urls_imat.py
    path('imat/', include('InscripcionResidenciaImagenes.urls_imat')),  # Enlaza a urls_imat.py

    # Rutas de administración
    path('admin/', admin.site.urls),
]

# Configuración para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
