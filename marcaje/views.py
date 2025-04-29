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
            params={'sucursal': 1},
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
    empleados = Empleado.objects.all()

    context = {
        'empleados': empleados,
    }
    return render(request, 'empleados.html', context)

def probando(request):
    return HttpResponse("HOLA PROBANDO")

def lista_registros(request):
    registros = RegistroMarcaje.objects.all()
    empleados = Empleado.objects.all()
    # sucursal = request.GET.get('sucursal')
    # departamento = request.GET.get('departamento')

    # if sucursal:
    #     registros = registros.filter(empleado__sucursal__id=sucursal)
    # if departamento:
    #     registros = registros.filter(empleado__departamento__id=departamento)

    context = {
        'registros': registros,
        'empleados': empleados,
        # 'departamentos': Departamentos.objects.all(),
        # 'sucursales': Sucursal.objects.all(),
        # 'departamento_seleccionado': departamento,
        # 'sucursal__seleccionada': sucursal,
    }

    return render(request, 'reporte.html', context)
# Create your views here.

