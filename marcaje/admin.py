from django.contrib import admin
from .models import *

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'sucursal')
    search_fields = ('codigo', 'sucursal')

@admin.register(Departamentos)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'departamento')
    search_fields = ('codigo', 'departamento')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'sucursal', 'departamento', 'horaentrada', 'horasalida')
    search_fields = ('codigo', 'nombre', 'sucursal', 'departamento')

@admin.register(RegistroMarcaje)
class RegistroMarcajeAdmin(admin.ModelAdmin):
    list_display = ('empleado','empleado__sucursal', 'fecha', 'marca_entrada', 'marca_salida', 'simbolo', 'falta', 'empleado__departamento')
    list_filter = ('fecha', 'empleado__departamento', 'empleado__sucursal')
    search_fields = ('empleado__codigo', 'empleado__nombre')
    date_hierarchy = 'fecha'
