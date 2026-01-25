from django.db import models
from apps.usuarios.models import Usuarios
from apps.clientes.models import Clientes
from apps.productos.models import Productos
from django.conf import settings

class Ventas(models.Model):
    cliente_id = models.ForeignKey(Clientes, on_delete=models.PROTECT)
    usuario_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha = models.DateField()
    estado = models.BooleanField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.fecha)

class Facturas(models.Model):

    venta_id = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    numero_factura = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )
    fecha_emision = models.DateField(auto_now_add=True)
    estado = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.numero_factura:
            ultimo = Facturas.objects.order_by('-id').first()
            siguiente_numero = 1 if not ultimo else ultimo.id + 1
            self.numero_factura = str(siguiente_numero).zfill(20)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero_factura

class Detalle_Ventas(models.Model):
    venta_id = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto_id.nombre} - {self.sub_total}"

class Devoluciones(models.Model):
    usuario_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    venta_id = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    cliente_id = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.BooleanField()
    motivo = models.CharField(max_length=150)

class Detalle_Devoluciones(models.Model):
    devolucion_id = models.ForeignKey(Devoluciones, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    observacion = models.CharField(max_length=150)
