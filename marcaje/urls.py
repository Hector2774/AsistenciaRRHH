from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_registros),
    path('/sync-empleados/', views.sync_empleados_view, name='sync_empleados'),
    path('/api/empleados/', views.empleados_proxy, name='empleados_proxy'),
    path('/registrados', views.marcar)
   
]