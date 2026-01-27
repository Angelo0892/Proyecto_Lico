from django.contrib import admin
from .models import (
    Usuario, Cliente, Proveedor, Producto, Categoria, Ubicacion,
    Venta, DetalleVenta, Factura, Pago, Importacion, DetalleImportacion,
    MetodoPago, Rol, Permiso, Auditoria, Devolucion, DetallePago
)

# Configuración básica para que se vean bonitos en el admin
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido1', 'ci', 'tipo_cliente')
    search_fields = ('nombre', 'ci', 'nit')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'stock_actual', 'precio_venta', 'ubicacion')
    search_fields = ('nombre', 'codigo')
    list_filter = ('categoria', 'proveedor')

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'total', 'estado')
    inlines = [DetalleVentaInline]
    list_filter = ('estado', 'fecha')

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'fecha_emision', 'monto_total', 'estado')

# Registrar el resto de modelos simples
admin.site.register(Usuario)
admin.site.register(Proveedor)
admin.site.register(Categoria)
admin.site.register(Ubicacion)
admin.site.register(MetodoPago)
admin.site.register(Pago)
admin.site.register(Importacion)
admin.site.register(Rol)
admin.site.register(Permiso)
admin.site.register(Auditoria)
admin.site.register(Devolucion)
admin.site.register(DetallePago)