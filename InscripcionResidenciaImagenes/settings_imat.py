import environ
import os
from pathlib import Path

# Definición de BASE_DIR para las rutas relativas
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración del entorno
env = environ.Env()
environ.Env.read_env()  # Cargar las variables del archivo .env

# Clave secreta de Django
SECRET_KEY = env("DJANGO_SECRET_KEY")

# Debugging
DEBUG = env.bool("DEBUG", default=True)  # Asegúrate de ajustar esto en producción

# Base de datos
DATABASES = {
    'default': env.db("DATABASE_URL")
}

# Configuración de Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env("CLOUDINARY_CLOUD_NAME"),
    'API_KEY': env("CLOUDINARY_API_KEY"),
    'API_SECRET': env("CLOUDINARY_API_SECRET"),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Configuración de correo
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")

# Zona horaria e idioma
TIME_ZONE = 'America/Argentina/Buenos_Aires'
LANGUAGE_CODE = 'es-ar'
USE_I18N = True
USE_TZ = True

# Configuración específica para el sitio de Imat
SITE_ID = 2
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'imat-residencia-cb65ac618754.herokuapp.com']

# Configuración de URLs
ROOT_URLCONF = 'InscripcionResidenciaImagenes.urls'

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Mis aplicaciones
    'asistencia.apps.AsistenciaConfig',
    'casos_interesantes_db.apps.CasosInteresantesDbConfig',
    'facturacion.apps.FacturacionConfig',
    'imat.apps.ImatConfig',
    # Aplicaciones de terceros
    'taggit',
]

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'asistencia.Usuario'

# Redirección de inicio de sesión
LOGIN_REDIRECT_URL = 'home'

# Validadores de contraseña
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

# Configuración de plantillas
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

# Middleware
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

# Archivos estáticos y de medios
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'asistencia', 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Tipo de campo de clave principal predeterminado
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
