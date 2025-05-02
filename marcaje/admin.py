from django.contrib import admin
from .models import *

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'sucursal', 'departamento')
    search_fields = ('codigo', 'nombre', 'sucursal', 'departamento')
    list_filter = ('codigo', 'nombre', 'sucursal', 'departamento')

@admin.register(Marcaje)
class MarcajeAdmin(admin.ModelAdmin):
    list_display = ('empleado__codigo', 'empleado', 'fecha_hora', 'empleado__sucursal', 'tipo_registro', 'empleado__departamento')
     

@admin.register(RegistroMarcaje)
class RegistroMarcajeAdmin(admin.ModelAdmin):
    list_display = ('empleado','empleado__sucursal', 'fecha', 'marca_entrada', 'marca_salida', 'simbolo', 'falta', 'empleado__departamento')
    list_filter = ('fecha', 'empleado__departamento', 'empleado__sucursal')
    search_fields = ('empleado__codigo', 'empleado__nombre')
    date_hierarchy = 'fecha'
