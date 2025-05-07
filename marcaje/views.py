from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from .models import *
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from .sync import sincronizar_empleados
from .sync_marcaje import sincronizar_marcajes
from django.core import serializers
from django.views.decorators.http import require_POST
from datetime import datetime
from django.utils import timezone
from .depurar_marcajes import depurar_marcajes
from .forms import *

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


@require_POST
def sync_marcaje_view(request):
    try:
        # Ejecutar tu función de sincronización
        fecha_str = request.GET.get('fecha') or timezone.now().strftime('%Y-%m-%d')
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        resultado = sincronizar_marcajes(fecha=fecha)
        
        # Si hay error en la sincronización
        if 'error' in resultado:
            return JsonResponse({
                'status': 'error',
                'message': resultado['error'],
                'marcajes': []
            }, status=400)
        
        depurar_marcajes(fecha)
        # Obtener marcajes recién sincronizados
        marcajes = Marcaje.objects.all().order_by('-fecha_hora')
        
        # Preparar respuesta compatible con tu frontend
        return JsonResponse({
            'status': 'success',
            'message': f'Sincronización completada para {fecha_str}',
            'creados': resultado.get('creados', 0),
            'actualizados': resultado.get('actualizados', 0),
            'errores': resultado.get('errores', 0),
            'marcajes': serializers.serialize('json', marcajes)
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'marcajes': []
        }, status=500)


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
    return render(request, 'validar_asistencia.html')

def lista_registros(request):
    registros = Marcaje.objects.all()
    departamento = request.GET.get('departamento')
    empleados = Empleado.objects.all()
    
   
    if departamento:
        registros = registros.filter(empleado__departamento=departamento)
   
    departamentos = Empleado.objects.order_by('departamento'
                      ).values_list('departamento', flat=True
                      ).distinct()
    context = {
        'registros': registros,
        'empleados': empleados,
        'departamentos': departamentos,
        
        'departamento_seleccionado': departamento,
        # 'sucursal__seleccionada': sucursal,
    }

    return render(request, 'reporte.html', context)
# Create your views here.

def validar_asistencias(request):
    if request.method == 'GET':
        sucursales = Sucursal.objects.all()
        return render(request, 'validar_asistencia.html', {'sucursales': sucursales})
    
    # Para solicitudes AJAX
    try:
        data = request.POST
        sucursal_id = data.get('sucursal')
        fecha_str = data.get('fecha')
        
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        empleados = Empleado.objects.filter(sucursal_id=sucursal_id)
        resultados = []
        
        for empleado in empleados:
            marcaje_depurado = MarcajeDepurado.objects.filter(
                empleado=empleado,
                fecha=fecha
            ).first()
            
            resultados.append({
                'fecha': fecha,
                'sucursal': empleado.sucursal.nombre,
                'codigo': empleado.codigo,
                'nombre': empleado.nombre,
                'departamento': empleado.departamento,
                'asistio': marcaje_depurado is not None,  # True si hay registro depurado
                'entrada': marcaje_depurado.entrada.strftime('%H:%M') if marcaje_depurado and marcaje_depurado.entrada else '--',
                'salida': marcaje_depurado.salida.strftime('%H:%M') if marcaje_depurado and marcaje_depurado.salida else '--',
            })
        
        return JsonResponse({'data': resultados})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def vista_solicitud(request):
    return render(request, 'solicitud_permiso.html')

def crear_permiso(request):
    sucursales = Sucursal.objects.all()
    departamentos = Empleado.objects.order_by('departamento'
                      ).values_list('departamento', flat=True
                      ).distinct()

    if request.method == 'POST':
        try:
            empleado_id = request.POST.get('empleado')
            tipo_permiso = request.POST.get('tipo_permiso')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_final = request.POST.get('fecha_final')
            descripcion = request.POST.get('descripcion')
            comprobante = request.FILES.get('comprobante')

            empleado = Empleado.objects.get(id=empleado_id)

            Permisos.objects.create(
                empleado=empleado,
                tipo_permiso=tipo_permiso,
                fecha_inicio=fecha_inicio,
                fecha_final=fecha_final,
                descripcion=descripcion,
                comprobante=comprobante
            )

            return redirect('crear_permiso')  # O a una página de éxito

        except Empleado.DoesNotExist:
            return HttpResponseBadRequest("Empleado no válido")
        except Exception as e:
            return HttpResponseBadRequest(f"Error al guardar: {e}")
        
    return render(request, 'crear_permiso.html', {
        'sucursales': sucursales,
        'departamentos': departamentos
    })

def obtener_empleados(request):
    sucursal_id = request.GET.get('sucursal_id')
    departamento = request.GET.get('departamento')

    empleados = Empleado.objects.filter(
        sucursal_id=sucursal_id,
        departamento=departamento
    ).values('id', 'nombre')

    return JsonResponse(list(empleados), safe=False)