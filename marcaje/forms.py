from django import forms
from .models import Permisos, Empleado
from django_select2.forms import ModelSelect2Widget

class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permisos
        fields = ['empleado','tipo_permiso', 'fecha_inicio', 'fecha_final', 'descripcion', 'comprobante']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date'}),
            'empleado': ModelSelect2Widget(
                model=Empleado,
                search_fields=['nombre__icontains'],  # O los campos que quieras buscar
            )
        }
