from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Conecta todas las rutas de la app NUAM
    path('', include('nuam.urls')),
]
