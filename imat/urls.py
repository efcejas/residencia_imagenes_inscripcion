
# imat/urls.py
from django.urls import path
from .views import InicioImatView

app_name = 'imat'

urlpatterns = [
    # path('', InicioImatView.as_view(), name='inicioimat'),  # Página de inicio específica de Imat
]
