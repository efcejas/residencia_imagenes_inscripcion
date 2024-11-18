from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from imat.views import RegistroImatView, RegistroExitosoImatView

urlpatterns = [
    # Administración
    path('admin/', admin.site.urls),

    # URLs de la aplicación IMAT
    path('', include('imat.urls', namespace='imat')),

    # Autenticación específica para IMAT
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration-imat/login.html'), name='login_imat'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration-imat/logged_out.html'), name='logout_imat'),
    path('accounts/register/', RegistroImatView.as_view(), name='register_imat'),
    path('accounts/register_success/', RegistroExitosoImatView.as_view(), name='register_success_imat'),
]
