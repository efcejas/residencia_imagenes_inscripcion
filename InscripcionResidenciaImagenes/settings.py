"""
Configuración de Django para el proyecto InscripcionResidenciaImagenes.

Generado por 'django-admin startproject' usando Django 5.0.3.

Para obtener más información sobre este archivo, consulte
https://docs.djangoproject.com/en/5.0/topics/settings/

Para obtener la lista completa de configuraciones y sus valores, consulte
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from decouple import config
import dj_database_url

load_dotenv()

# Construya rutas dentro del proyecto de esta manera: BASE_DIR /'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de desarrollo de inicio rápido: no adecuada para producción
# Ver https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: ¡mantenga en secreto la clave secreta utilizada en la producción!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# ADVERTENCIA DE SEGURIDAD: ¡no ejecute con la depuración activada en producción!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'residentes-dm-9833103dde7d.herokuapp.com']

# Definición de aplicación
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites', # Para activar el uso de sitios
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Mis aplicaciones
    'asistencia.apps.AsistenciaConfig', # Se pone .apps.AsistenciaConfig para que sepa que es una aplicacion y cumpla con el estandar de Django
    'casos_interesantes_db.apps.CasosInteresantesDbConfig',
    'facturacion.apps.FacturacionConfig',  # Nueva aplicación
    # Aplicaciones de terceros
    'taggit',
]

SITE_ID = 1 # Del sitio actual

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'InscripcionResidenciaImagenes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'asistencia/templates', BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'InscripcionResidenciaImagenes.wsgi.application'

# Base de datos
DATABASES = {
    'default': dj_database_url.config(default='postgres://postgres:efc8563456@localhost:5432/gestion_residentes')
}

# Registro de modelos personalizados
AUTH_USER_MODEL = 'asistencia.Usuario'

# Redirección de URLs inicio
LOGIN_REDIRECT_URL = 'home'

# Validación de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuración de correo electrónico
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# Internacionalización
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JavaScript, Imágenes)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'asistencia', 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

import cloudinary
import cloudinary.uploader
import cloudinary.api
import cloudinary_storage
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary_storage.storage import RawMediaCloudinaryStorage

# Configuración de Cloudinary

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Archivos de medios
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Tipo de campo de clave principal predeterminado
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'