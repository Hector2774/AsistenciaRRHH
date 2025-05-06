from django import forms
from .models import Permisos

class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permisos
        fields = ['empleado','tipo_permiso', 'fecha_inicio', 'fecha_final', 'descripcion', 'comprobante']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date'}),
        }