from django.shortcuts import render
from django.http import HttpResponse
from .models import RegistroMarcaje

def marcar(request):
    return render(request, 'reporte.html')

def probando(request):
    return HttpResponse("HOLA PROBANDO")

def lista_registros(request):
     registros = RegistroMarcaje.objects.all().order_by('-fecha', 'empleado__nombre')
     return render(request, 'reporte.html', {'registros': registros})
# Create your views here.