# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    pais_origen = models.CharField(max_length=100)
    contacto = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    calificacion = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.nombre} - {self.pais_origen}"

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categorías de Productos"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPOS_ALCOHOL = [
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

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS_ALCOHOL)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.SET_NULL, null=True)
    marca = models.CharField(max_length=100)
    volumen_ml = models.IntegerField()
    graduacion_alcoholica = models.DecimalField(max_digits=4, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=10)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

    @property
    def margen_ganancia(self):
        if self.precio_compra > 0:
            return ((self.precio_venta - self.precio_compra) / self.precio_compra) * 100
        return 0

    @property
    def necesita_reorden(self):
        return self.stock_actual <= self.stock_minimo

class ImportacionLote(models.Model):
    ESTADOS = [
        ('PLANIFICADO', 'Planificado'),
        ('EN_TRANSITO', 'En Tránsito'),
        ('ADUANA', 'En Aduana'),
        ('RECIBIDO', 'Recibido'),
        ('CANCELADO', 'Cancelado'),
    ]

    numero_lote = models.CharField(max_length=50, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_orden = models.DateField()
    fecha_estimada_llegada = models.DateField()
    fecha_llegada_real = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PLANIFICADO')
    costo_total = models.DecimalField(max_digits=12, decimal_places=2)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2)
    costo_aduana = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField(blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Lotes de Importación"

    def __str__(self):
        return f"Lote {self.numero_lote} - {self.proveedor.nombre}"

    @property
    def costo_total_completo(self):
        return self.costo_total + self.costo_envio + self.costo_aduana

class DetalleImportacion(models.Model):
    lote = models.ForeignKey(ImportacionLote, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

class Cliente(models.Model):
    TIPOS_CLIENTE = [
        ('MINORISTA', 'Minorista'),
        ('MAYORISTA', 'Mayorista'),
        ('DISTRIBUIDOR', 'Distribuidor'),
        ('RESTAURANTE', 'Restaurante/Bar'),
    ]

    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS_CLIENTE)
    ruc_dni = models.CharField(max_length=20, unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class Venta(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('PARCIAL', 'Pago Parcial'),
        ('CANCELADO', 'Cancelado'),
    ]

    METODOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('TARJETA', 'Tarjeta'),
        ('CREDITO', 'Crédito'),
    ]

    numero_factura = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Venta {self.numero_factura} - {self.cliente.nombre}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def subtotal(self):
        return (self.cantidad * self.precio_unitario) * (1 - self.descuento / 100)