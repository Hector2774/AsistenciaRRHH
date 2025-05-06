from django.db import models


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.nombre}"

class Empleado(models.Model):
    id_externo = models.IntegerField(unique=True)
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['nombre']

    
    def __str__(self):
        return f"{self.nombre} "
 
class Marcaje(models.Model):
    TIPO_REGISTRO = [
        ('I', 'Entrada'),
        ('O', 'Salida'),
    ]

    empleado = models.ForeignKey(
        'Empleado',
       
        on_delete=models.CASCADE,
        
        verbose_name="Empleado"
    )
    fecha_hora = models.DateTimeField(verbose_name="Fecha y hora de registro")
    tipo_registro = models.CharField(
        max_length=1,
        choices=TIPO_REGISTRO,
        verbose_name="Tipo de marcaje"
    )



    def __str__(self):
        return f"{self.empleado.codigo} - {self.fecha_hora} ({self.get_tipo_registro_display()})"


class MarcajeDepurado(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField()
    entrada = models.TimeField(null=True)
    salida = models.TimeField(null=True)
   
    def __str__(self):
        return self.empleado.codigo