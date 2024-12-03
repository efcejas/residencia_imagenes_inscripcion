from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from imat.views import RegistroImatView, RegistroExitosoImatView

urlpatterns = [
    # Administración (con prefijo único)
    path('imat-admin/', admin.site.urls),

    # URLs de la aplicación IMAT
    path('', include(('imat.urls', 'imat'), namespace='imat')),

    # Autenticación específica para IMAT
    path('imat/accounts/login/', auth_views.LoginView.as_view(template_name='registration-imat/login.html'), name='login_imat'),
    path('imat/accounts/logout/', auth_views.LogoutView.as_view(template_name='registration-imat/logged_out.html'), name='logout_imat'),
    path('imat/accounts/register/', RegistroImatView.as_view(), name='register_imat'),
    path('imat/accounts/register_success/', RegistroExitosoImatView.as_view(), name='register_success_imat'),
]
