from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_registros),
    path('/emp', views.marcar),
    path('/api/empleados/', views.empleados_proxy, name='empleados_proxy'),
]