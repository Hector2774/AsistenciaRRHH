from django.db import models

from django.db import models

class Sucursal(models.Model):
    codigo = models.CharField(max_length=20, unique=True, primary_key=True)
    sucursal = models.CharField(max_length=100)

    def __str__(self):
        return self.sucursal

class Departamentos(models.Model):
    codigo = models.CharField(max_length=20, unique=True, primary_key=True)
    departamento = models.CharField(max_length=100)

    def __str__(self):
        return self.departamento

class Empleado(models.Model):
    # Campo alfanumérico como especificó tu supervisor
    codigo = models.CharField(max_length=20, unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT, null=True, blank=True)
    departamento = models.ForeignKey(Departamentos, on_delete=models.PROTECT, null=True, blank=True)
    horaentrada = models.TimeField(null=True, blank=True)
    horasalida = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre} "

class RegistroMarcaje(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    marca_entrada = models.TimeField(null=True, blank=True)
    marca_salida = models.TimeField(null=True, blank=True)
    simbolo = models.CharField(max_length=2, null=True, blank=True)
    falta = models.BooleanField(default=False)
   
    class Meta:
        verbose_name_plural = "Registros de Marcaje"
    
    def save(self, *args, **kwargs):
        self.falta = self.simbolo == "A"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.empleado.codigo} - {self.fecha}"
