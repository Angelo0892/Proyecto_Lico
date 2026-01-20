from django.db import models
from apps.ventas.models import Facturas
from apps.productos.models import Productos

class Metodos_Pago(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Pagos(models.Model):
    factura_id = models.ForeignKey(Facturas, on_delete=models.CASCADE)
    factura_registro = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.factura_registro)

class Detalle_Pagos(models.Model):
    pago_id = models.ForeignKey(Pagos, on_delete=models.CASCADE)
    metodo_pago_id = models.ForeignKey(Metodos_Pago, on_delete=models.CASCADE)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    referencia_transaccion = models.CharField(max_length=50)

    def __str__(self):
        return self.referencia_transaccion