from django.shortcuts import render
from django.http import HttpResponse
from .models import RegistroMarcaje, Departamentos, Sucursal
from django.db.models import Q
import requests
from django.http import JsonResponse


def empleados_proxy(request):
    sucursal_id = 1 

    if not sucursal_id:
        return JsonResponse({'error': 'No se especificó la sucursal'}, status=400)

    # Construir la URL del servidor externo
    url = f'http://192.168.11.185:3003/planilla/webservice/empleados/?sucursal={sucursal_id}'

    try:
        # Hacer la petición al servidor externo
        response = requests.get(url, headers={'X-Requested-With': 'XMLHttpRequest'})
        response.raise_for_status()  # Lanza error si la respuesta es 4xx o 5xx
        data = response.json()  # Convertimos la respuesta en JSON
    except requests.exceptions.RequestException as e:
        # Si hubo un error al conectarse
        return JsonResponse({'error': str(e)}, status=500)

    # Devolver la data al navegador
    return JsonResponse(data, safe=False)

def marcar(request):
    return render(request, 'empleado.html')

def probando(request):
    return HttpResponse("HOLA PROBANDO")

def lista_registros(request):
    registros = RegistroMarcaje.objects.all()
    sucursal = request.GET.get('sucursal')
    departamento = request.GET.get('departamento')

    if sucursal:
        registros = registros.filter(empleado__sucursal__id=sucursal)
    if departamento:
        registros = registros.filter(empleado__departamento__id=departamento)

    context = {
        'registros': registros,
        'departamentos': Departamentos.objects.all(),
        'sucursales': Sucursal.objects.all(),
        'departamento_seleccionado': departamento,
        'sucursal__seleccionada': sucursal,
    }

    return render(request, 'reporte.html', context)
# Create your views here.