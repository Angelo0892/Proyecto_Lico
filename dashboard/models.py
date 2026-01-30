from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator

# ==========================================
# 1. CATALOGOS Y CONFIGURACIÓN
# ==========================================
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Ubicaciones"
    def __str__(self): return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150, blank=True, null=True)

    PERMISOS_DEFECTO = [
        ("modulo_dashboard", "Acceso al dashboard principal"),
        ("modulo_usuarios", "Gestión de usuarios"),
        ("modulo_categorias", "Gestión de categorías de productos"),
        ("modulo_facturacion", "Facturación y ventas"),
        ("modulo_proveedores", "Gestión de proveedores"),
        ("modulo_clientes", "Gestión de clientes"),
        ("modulo_inventario", "Gestión de productos"),
        ("modulo_importacion", "Gestión de importaciones"),
        ("modulo_ventas", "Gestión de ventas"),
        ("modulo_reportes", "Acceso a reportes"),
    ]

    class Meta:
        verbose_name_plural = "Categorías"
    def __str__(self): return self.nombre

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Métodos de Pago"
    def __str__(self): return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    permisos = models.ManyToManyField('Permiso', blank=True)

    class Meta:
        verbose_name_plural = "Roles"
    def __str__(self): return self.nombre

class Permiso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self): return self.nombre

# ==========================================
# 2. ACTORES DEL SISTEMA
# ==========================================
class Usuario(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        null=True,
        blank=True
    )

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def tiene_permiso(self, permiso):
        if not self.rol:
            return False
        return self.rol.permisos.filter(nombre=permiso).exists()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50, blank=True, null=True)
    ci = models.CharField(max_length=20, unique=True, verbose_name="CI")
    nit = models.CharField(max_length=20, blank=True, null=True, verbose_name="NIT")
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    tipo_cliente = models.CharField(max_length=20, choices=[('MINORISTA', 'Minorista'), ('MAYORISTA', 'Mayorista')], default='MINORISTA')
    
    # Campo extra para que funcione tu dashboard (aunque no esté en el diagrama original es vital)
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Clientes"
    def __str__(self): return f"{self.nombre} {self.apellido1}"

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_proveedor = models.CharField(max_length=200, blank=True, null=True) # Según diagrama
    contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True) # Para dashboard "pais_origen"
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Proveedores"
    def __str__(self): return self.nombre

# ==========================================
# 3. PRODUCTOS E INVENTARIO
# ==========================================
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=50, unique=True) # Vital para inventario
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True)
    
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_actual = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(default=5, validators=[MinValueValidator(0)])
    
    # Campo extra para compatibilidad con dashboard
    tipo = models.CharField(max_length=20, default='Varios') # VINO, RON, etc.
    marca = models.CharField(max_length=50, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self): return self.nombre

class Importacion(models.Model): # Tabla Importaciones
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_pedido = models.DateField()
    fecha_llegada = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, default='PLANIFICADO')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    observacion = models.TextField(blank=True, null=True)

    stock_ingresado = models.BooleanField(default=False)
    
    # Alias para dashboard (ImportacionLote usa estos nombres)
    @property
    def numero_lote(self): return f"IMP-{self.id}"
    @property
    def costo_total(self): return self.total
    @property
    def fecha_estimada_llegada(self): return self.fecha_llegada or self.fecha_pedido

    class Meta:
        verbose_name_plural = "Importaciones"
    def __str__(self): return f"Importación {self.id}"

class DetalleImportacion(models.Model):
    importacion = models.ForeignKey(Importacion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)])
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name_plural = "Detalles de Importación"

# ==========================================
# 4. VENTAS, FACTURACIÓN Y PAGOS
# ==========================================
class Venta(models.Model):
    # 1. DEFINIMOS LAS OPCIONES AQUÍ ARRIBA
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado / Exitoso'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    observacion = models.TextField(blank=True, null=True)
    
    # 2. VINCULAMOS LAS OPCIONES AL CAMPO 'estado'
    # Agrega "choices=ESTADOS" en esta línea:
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

class Factura(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    numero_factura = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    nit_cliente = models.CharField(max_length=20)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estado = models.BooleanField(default=True) # Activa/Anulada

    def __str__(self): return f"Factura {self.numero_factura}"

class Pago(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=100, blank=True, null=True) # Nro recibo/transaccion

    def __str__(self): return f"Pago {self.id}"

class DetallePago(models.Model):
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=150)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

# ==========================================
# 5. DEVOLUCIONES Y AUDITORIA
# ==========================================
class Devolucion(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField()
    total_reembolsado = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estado = models.CharField(max_length=20, default='PENDIENTE')

    class Meta:
        verbose_name_plural = "Devoluciones"

class DetalleDevolucion(models.Model):
    devolucion = models.ForeignKey(Devolucion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)])
    observacion = models.CharField(max_length=150, blank=True)

class Auditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=50) # Crear, Editar, Eliminar
    tabla = models.CharField(max_length=50) # En qué tabla ocurrió
    registro_id = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    detalle = models.TextField(blank=True, null=True) # JSON o texto del cambio