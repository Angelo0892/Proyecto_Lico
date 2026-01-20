from django.db import models
from apps.usuarios.models import Usuarios
from apps.productos.models import Productos
from django.conf import settings


class Proveedores(models.Model):
    nit = models.CharField(max_length=20)
    tipo_proveedor = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50, null=True)
    apellido2 = models.CharField(max_length=50, null=True)
    pais = models.CharField(max_length=50)
    contacto = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.nombre} - {self.pais}"

class Importaciones(models.Model):
    usuario_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    proveedor_id = models.ForeignKey(Proveedores, on_delete=models.PROTECT)
    fecha = models.DateField()
    estado = models.BooleanField()
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.costo_total)

class Detalle_Importaciones(models.Model):
    importacion_id = models.ForeignKey(Importaciones, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Productos, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto_id.nombre} - {self.cantidad} unidades"
