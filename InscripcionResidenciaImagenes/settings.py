"""
Configuración de Django para el proyecto InscripcionResidenciaImagenes.

Generado por 'django-admin startproject' usando Django 5.0.3.

Para obtener más información sobre este archivo, consulte
https://docs.djangoproject.com/en/5.0/topics/settings/

Para obtener la lista completa de configuraciones y sus valores, consulte
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Construya rutas dentro del proyecto de esta manera: BASE_DIR /'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de desarrollo de inicio rápido: no adecuada para producción
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: ¡mantenga en secreto la clave secreta utilizada en la producción!
SECRET_KEY = 'django-insecure-k1zf!dv103jcip%ibsu@lu-2a)lpn3pcc=y-3fhr)=k5bxhi4&'

# ADVERTENCIA DE SEGURIDAD: ¡no ejecute con la depuración activada en producción!
DEBUG = True

ALLOWED_HOSTS = ['192.168.0.71', 'localhost', '127.0.0.1']


# Definición de aplicación

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Mis aplicaciones
    'encuestas.apps.EncuestasConfig', # Aplicacion para encuestas
    'asistencia.apps.AsistenciaConfig', # Se poner .apps.AsistenciaConfig para que sepa que es una aplicacion y cumpla con el estandar de Django
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'InscripcionResidenciaImagenes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Ruta de los templates
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
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validación de contraseña
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internacionalización
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True


# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Tipo de campo de clave principal predeterminado
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
