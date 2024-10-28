from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('imat.urls', namespace='imat')),  # Incluye las URLs de imat con el namespace 'imat'
]

