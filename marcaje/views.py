from django.shortcuts import render
from django.http import HttpResponse
from .models import RegistroMarcaje, Empleado
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from .sync import sincronizar_empleados
from django.core import serializers

def empleados_proxy(request):
    target_url = "http://192.168.11.185:3003/planilla/webservice/empleados/"
    
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json',
    }
    
    try:
        response = requests.get(
            target_url,
            headers=headers,
            params={'sucursal': 2},
            timeout=10
        )
        response.raise_for_status()
        return JsonResponse(response.json())
    
    except Exception as e:
        return JsonResponse(
            {'error': str(e)},
            status=500
        )
# @csrf_exempt    
def sync_empleados_view(request):
    if request.method == 'POST':
        resultado = sincronizar_empleados()

        empleados = Empleado.objects.all()
        empleados_json = serializers.serialize('json', empleados)
            
        resultado['empleados'] = empleados_json  # Agrega los datos al resultado
        return JsonResponse(resultado)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def marcar(request):
    departamento = request.GET.get('departamento')
    empleados = Empleado.objects.all()

    if departamento:
        empleados = empleados.filter(departamento=departamento)
    
    departamentos = Empleado.objects.order_by('departamento'
                      ).values_list('departamento', flat=True
                      ).distinct()

    context = {
        'empleados': empleados,
        'departamentos': departamentos,
        
        'departamento_seleccionado': departamento,
    }
    return render(request, 'empleados.html', context)

def probando(request):
    return HttpResponse("HOLA PROBANDO")

def lista_registros(request):
    registros = RegistroMarcaje.objects.all()
    departamento = request.GET.get('departamento')
    empleados = Empleado.objects.all()
    
   
    if departamento:
        registros = registros.filter(empleado__departamento=departamento)
   
    departamentos = RegistroMarcaje.objects.values_list('empleado__departamento', flat=True).distinct()

    context = {
        'registros': registros,
        'empleados': empleados,
        'departamentos': departamentos,
        
        'departamento_seleccionado': departamento,
        # 'sucursal__seleccionada': sucursal,
    }

    return render(request, 'reporte.html', context)
# Create your views here.

