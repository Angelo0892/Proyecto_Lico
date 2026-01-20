# admin.py
from django.contrib import admin


"""
from .models import (
    Proveedores, Categorias, Productos, Importaciones,
    Detalle_Importaciones, Clientes, Ventas, Detalle_Ventas
)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais_origen', 'email', 'telefono', 'calificacion', 'activo']
    list_filter = ['pais_origen', 'activo', 'fecha_registro']
    search_fields = ['nombre', 'email', 'pais_origen']
    list_editable = ['activo', 'calificacion']
    ordering = ['-calificacion', 'nombre']

@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'tipo', 'marca', 'stock_actual', 'stock_minimo', 
                    'precio_compra', 'precio_venta', 'proveedor', 'activo']
    list_filter = ['tipo', 'activo', 'proveedor', 'categoria']
    search_fields = ['codigo', 'nombre', 'marca']
    list_editable = ['stock_actual', 'precio_venta', 'activo']
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'tipo', 'categoria', 'marca', 'activo')
        }),
        ('Detalles del Producto', {
            'fields': ('volumen_ml', 'graduacion_alcoholica', 'proveedor')
        }),
        ('Inventario', {
            'fields': ('stock_actual', 'stock_minimo')
        }),
        ('Precios', {
            'fields': ('precio_compra', 'precio_venta')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('proveedor', 'categoria')

class DetalleImportacionInline(admin.TabularInline):
    model = DetalleImportacion
    extra = 1
    autocomplete_fields = ['producto']

@admin.register(ImportacionLote)
class ImportacionLoteAdmin(admin.ModelAdmin):
    list_display = ['numero_lote', 'proveedor', 'fecha_orden', 'fecha_estimada_llegada', 
                    'estado', 'costo_total_completo', 'creado_por']
    list_filter = ['estado', 'proveedor', 'fecha_orden']
    search_fields = ['numero_lote', 'proveedor__nombre']
    readonly_fields = ['fecha_creacion', 'creado_por', 'costo_total_completo']
    inlines = [DetalleImportacionInline]
    
    fieldsets = (
        ('Información del Lote', {
            'fields': ('numero_lote', 'proveedor', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_orden', 'fecha_estimada_llegada', 'fecha_llegada_real')
        }),
        ('Costos', {
            'fields': ('costo_total', 'costo_envio', 'costo_aduana', 'costo_total_completo')
        }),
        ('Información Adicional', {
            'fields': ('notas', 'creado_por', 'fecha_creacion'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'ruc_dni', 'telefono', 'email', 'limite_credito', 'activo']
    list_filter = ['tipo', 'activo', 'fecha_registro']
    search_fields = ['nombre', 'ruc_dni', 'email']
    list_editable = ['activo', 'limite_credito']
    readonly_fields = ['fecha_registro']

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    autocomplete_fields = ['producto']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'cliente', 'fecha', 'total', 'estado', 
                    'metodo_pago', 'vendedor']
    list_filter = ['estado', 'metodo_pago', 'fecha', 'cliente__tipo']
    search_fields = ['numero_factura', 'cliente__nombre']
    readonly_fields = ['fecha']
    inlines = [DetalleVentaInline]
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información de la Venta', {
            'fields': ('numero_factura', 'cliente', 'fecha', 'vendedor')
        }),
        ('Montos', {
            'fields': ('subtotal', 'impuesto', 'total')
        }),
        ('Estado y Pago', {
            'fields': ('estado', 'metodo_pago')
        }),
        ('Notas', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change and not obj.vendedor:
            obj.vendedor = request.user
        super().save_model(request, obj, form, change)
"""