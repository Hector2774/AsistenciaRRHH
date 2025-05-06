from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_registros),
    path('/sync-empleados/', views.sync_empleados_view, name='sync_empleados'),
    path('/api/empleados/', views.empleados_proxy, name='empleados_proxy'),
    path('/registrados', views.marcar),
    path('/sync-marcaje/', views.sync_marcaje_view, name='sync_marcaje'),
    path('/validar-asistencia/', views.validar_asistencias, name='validar_asistencia'),
    path('/solicitud/', views.vista_solicitud),
    path('/crear-permiso', views.crear_permiso)
    # path('/validar/', views.validar_asistencias),
   
]