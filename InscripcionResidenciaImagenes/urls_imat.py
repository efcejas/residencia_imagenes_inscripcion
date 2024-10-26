# urls_imat.py
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='imat/inicioimat.html'), name='home_imat'),  # Página de inicio específica de Imat
    path('imat/', include(('imat.urls', 'imat'), namespace='imat')),  # Otras rutas de Imat
]
