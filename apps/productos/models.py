from django.db import models
from apps.inventario.models import Proveedores

class Categorias(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=50)
    detalle = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categorías de Productos"

    def __str__(self):
        return self.nombre

class Productos(models.Model):
    proveedor_id = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    categoria_id = models.ForeignKey(Categorias, on_delete=models.SET_NULL, null=True)
    ubicacion_id = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True)
    stock = models.IntegerField()
    nombre = models.CharField(max_length=80)
    marca = models.CharField(max_length=50)
    origen = models.CharField(max_length=50)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"
