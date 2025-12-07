from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Funciones protegidas principales
    path('calcular/', views.calcular_view, name='calcular'),
    path('insertar/', views.insertar_view, name='insertar'),
    path('eliminar/', views.eliminar_view, name='eliminar'),

    # Nuevas funcionalidades
    path('modificar/<int:registro_id>/', views.modificar_view, name='modificar'),
    path('cargar-archivo/', views.cargar_archivo_view, name='cargar_archivo'),

    # Auditoría
    path('auditoria/', views.auditoria_view, name='auditoria'),
]
