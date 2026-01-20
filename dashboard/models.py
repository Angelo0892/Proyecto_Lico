# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

"""
class Metodos_Pago(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    descripcion = models.CharField(max_length=100, null=False)

class Clientes(models.Model):
    ci = models.CharField(max_length=20, null=True)
    nit = models.CharField(max_length=20, null=True)
    tipo_cliente = models.CharField(max_length=20, null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellido1 = models.CharField(max_length=50, null=True)
    apellido2 = models.CharField(max_length=50, null=True)
    direccion = models.CharField(max_length=200, null=True)
    telefono = models.CharField(max_length=30, null=False)
    email = models.CharField(max_length=80, null=False)

    class Meta:
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre}"

class Roles(models.Model):
    nombre_rol = models.CharField(max_length=30, null=False)
    descripcion = models.CharField(max_length=200, null=False)

class Usuarios(models.Model):
    rol_id = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    nombre_usuario = models.CharField(max_length=50, null=False, unique=True)
    clave = models.CharField(max_length=150, null=False)
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50, null=False)
    apellido1 = models.CharField(max_length=50, null=False)
    Apellido2 = models.CharField(max_length=50, null=False)
    telefono = models.CharField(max_length=20, null=False)
    direccion = models.CharField(max_length=150, null=False)
    estado = models.BooleanField(null=False)

    def __str__(self):
        return self.nombre_usuario

class Permisos(models.Model):
    rol_id = models.ForeignKey(Roles, on_delete=models.CASCADE, null=False)
    nombre_premiso = models.CharField(max_length=50, null=False)
    descripcion = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.nombre_premiso} - {self.rol_id.nombre_rol}"

class Auditoria(models.Model):
    usuario_id = models.ForeignKey(Usuarios, on_delete=models.PROTECT, null=False)
    fecha = models.DateField(null=False)
    accion = models.CharField(max_length=100, null=False)
    detalle = models.CharField(max_length=200, null=False)

    def __str__(self):
        return f"{self.usuario_id.nombre_usuario - self.accion}"

class Ventas(models.Model):
    cliente_id = models.ForeignKey(Clientes, on_delete=models.PROTECT, null=False)
    usuario_id = models.ForeignKey(Usuarios, on_delete=models.PROTECT, null=False)
    fecha = models.DateField(null=False)
    estado = models.BooleanField(null=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return self.fecha

class Facturas(models.Model):
    venta_id = models.ForeignKey(Ventas, on_delete=models.CASCADE, null=False)
    numero_factura = models.CharField(max_length=20, null=False)
    fecha_emision = models.DateField(null=False)
    estado = models.BooleanField(null=False)

    def __str__(self):
        return self.numero_factura

class Pagos(models.Model):
    factura_id = models.ForeignKey(Facturas, on_delete=models.CASCADE, null=False)
    factura_registro = models.DateField(null=False)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return self.factura_registro

class Detalle_Pagos(models.Model):
    pago_id = models.ForeignKey(Pagos, on_delete=models.CASCADE, null=False)
    metodo_pago_id = models.ForeignKey(Metodos_Pago, on_delete=models.CASCADE, null=False)
    fecha = models.DateField(null=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    referencia_transaccion = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.referencia_transaccion
    

class Proveedores(models.Model):
    nit = models.CharField(max_length=20, null=False)
    tipo_preedor = models.CharField(max_length=20, null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellido1 = models.CharField(max_length=50, null=True)
    apellido2 = models.CharField(max_length=50, null=True)
    pais = models.CharField(max_length=50, null=False)
    contacto = models.CharField(max_length=200, null=False)
    telefono = models.CharField(max_length=20, null=False)
    correo = models.EmailField(null=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.nombre} - {self.pais}"

class Categorias(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    descripcion = models.CharField(max_length=150, null=True)

    CATEGORIAS_ALCOHOL = [
        ('VINO', 'Vino'),
        ('WHISKY', 'Whisky'),
        ('RON', 'Ron'),
        ('VODKA', 'Vodka'),
        ('TEQUILA', 'Tequila'),
        ('CERVEZA', 'Cerveza'),
        ('CHAMPAGNE', 'Champagne'),
        ('COGNAC', 'Cognac'),
        ('GIN', 'Gin'),
        ('LICOR', 'Licor'),
    ]

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
    proveedor_id = models.ForeignKey(Proveedores, on_delete=models.CASCADE, null=False)
    categoria_id = models.ForeignKey(Categorias, on_delete=models.SET_NULL, null=True)
    ubicacion_id = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True)
    stock = models.IntegerField(null=False)
    nombre = models.CharField(max_length=80, null=False)
    marca = models.CharField(max_length=50, null=False)
    origen = models.CharField(max_length=50, null=False)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

class Importaciones(models.Model):
    usuario_id = models.ForeignKey(Usuarios, on_delete=models.PROTECT, null=False)
    proveedor_id = models.ForeignKey(Proveedores, on_delete=models.PROTECT, null=False)
    fecha = models.DateField(null=False)
    estado = models.BooleanField(null=False)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return self.costo_total

class Detalle_Importaciones(models.Model):
    importacion_id = models.ForeignKey(Importaciones, on_delete=models.CASCADE, null=False)
    producto_id = models.ForeignKey(Productos, on_delete=models.PROTECT, null=False)
    cantidad = models.IntegerField(null=False)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"{self.producto_id.nombre} - {self.cantidad} unidades"

class Detalle_Ventas(models.Model):
    venta_id = models.ForeignKey(Ventas, on_delete=models.CASCADE, null=False)
    producto_id = models.ForeignKey(Productos, on_delete=models.CASCADE, null=False)
    cantidad = models.IntegerField(null=False)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"{self.producto_id.nombre} - {self.sub_total}"
    
class Devoluciones(models.Model):
    usuario_id = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=False)
    venta_id = models.ForeignKey(Ventas, on_delete=models.CASCADE, null=False)
    cliente_id = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=False)
    fecha = models.DateField(null=False)
    eatado = models.BooleanField(null=False)
    motivo = models.CharField(max_length=150, null=False)

class Detalle_Devoluciones(models.Model):
    devolucion_id = models.ForeignKey(Devoluciones, on_delete=models.CASCADE, null=False)
    producto_id = models.ForeignKey(Productos, on_delete=models.CASCADE, null=False)
    cantidad = models.IntegerField(null=False)
    observacion = models.CharField(max_length=150, null=False)
"""