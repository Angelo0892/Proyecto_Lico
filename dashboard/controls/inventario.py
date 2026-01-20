from datetime import timedelta
from django.db.models import Sum, Count, F
from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Productos, Detalle_Ventas
from ..forms import productos

@login_required
def inventario(request):
    
    stock_minimo = 40

    # CRUD de productos
    productos = Productos.objects.all(
    ).order_by('-nombre')

    # Valor total del inventario por producto
    valor_total_inventario = Productos.objects.all(
    ).annotate(
        cantidad=Count('id'),
        stock_total=Sum('stock'),
        valor_inventario=Sum(F('stock') * F('precio_unitario'))
    ).order_by('-stock_total')
    
    # Productos que necesitan reorden
    productos_reorden = Productos.objects.filter(
        stock__lte= stock_minimo,
    ).select_related('proveedor_id').order_by('stock')
    
    # Productos sin movimiento (últimos 30 días)
    hace_un_mes = timezone.now() - timedelta(days=30)

    # Productos en constante movimiento
    productos_con_ventas = Detalle_Ventas.objects.filter(
        venta_id__fecha__gte=hace_un_mes
    ).values_list('producto_id', flat=True).distinct()
    
    # Productos sin movimiento
    productos_sin_movimiento = Productos.objects.all(
    ).exclude(
        id__in=productos_con_ventas
    ).order_by('-stock')[:20]
    
    # Rotación de inventario por tipo
    # rotacion_por_tipo = []
    """
    for tipo_display in Productos.TIPOS_ALCOHOL:
    tipo_code = tipo_display[0]
    productos = Producto.objects.filter(tipo=tipo_code, activo=True)
    
    stock_promedio = productos.aggregate(Avg('stock_actual'))['stock_actual__avg'] or 0
    ventas_mes = DetalleVenta.objects.filter(
        producto__tipo=tipo_code,
        venta__fecha__gte=timezone.now() - timedelta(days=30)
    ).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    
    rotacion = (ventas_mes / stock_promedio) if stock_promedio > 0 else 0
    
    rotacion_por_tipo.append({
        'tipo': tipo_display[1],
        'stock_promedio': round(stock_promedio, 2),
        'ventas_mes': ventas_mes,
        'rotacion': round(rotacion, 2)
    })
    """
    context = {
        'productos': productos,
        'valor_total_inventario': valor_total_inventario,
        'productos_reorden': productos_reorden,
        'productos_sin_movimiento': productos_sin_movimiento,
        #'rotacion_por_tipo': rotacion_por_tipo,
    }

    return render(request, 'dashboard/inventario/inventario.html', context)

@login_required
def editar_producto(request, id):

    producto = get_object_or_404(Productos, id = id)

    form = productos.formulario_producto(instance=producto)

    context = {
        'producto': producto,
        'form': form,
    }

    return render(request, 'dashboard/inventario/producto.html', context)

@login_required
def eliminar_producto(request, id):
    Productos.objects.get(id = id).delete

    return redirect('inventario')

@login_required
def actualizar_producto(request, id):

    Productos.objects.get(id = id)

    return redirect('inventario')