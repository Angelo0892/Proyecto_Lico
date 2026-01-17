# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, F, Q, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth, TruncDate
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
from .models import (
    Productos, Ventas, Detalle_Ventas, Clientes, Proveedores,
    Importaciones, Detalle_Importaciones, Categorias
)

@login_required
def dashboard_principal(request):
    return render(request, 'dashboard/principal.html')

""" Modificar código para que se adapte al proyecto """
"""
@login_required
def dashboard_principal(request):
    
    # Filtros de fecha
    hoy = timezone.now().date()
    hace_30_dias = hoy - timedelta(days=30)
    mes_actual = hoy.replace(day=1)
    
    # Métricas de ventas
    ventas_mes = Ventas.objects.filter(
        fecha__gte=mes_actual,
        estado__in=['True']
    )
    
    total_ventas_mes = ventas_mes.aggregate(
        total=Sum('total')
    )['total'] or 0
    
    ventas_hoy = Ventas.objects.filter(
        fecha__date=hoy,
        estado__in=['True']
    )
    
    total_ventas_hoy = ventas_hoy.aggregate(
        total=Sum('total')
    )['total'] or 0
    
    # Productos más vendidos este mes
    productos_top = Detalle_Ventas.objects.filter(
        venta__fecha__gte=mes_actual,
        venta__estado__in=['True']
    ).values(
        'producto__nombre',
        'producto__marca',
        'producto__tipo'
    ).annotate(
        cantidad_vendida=Sum('cantidad'),
        ingresos=Sum(F('cantidad') * F('precio_unitario'))
    ).order_by('-cantidad_vendida')[:10]
    
    # Inventario crítico
    productos_bajo_stock = Productos.objects.filter(
        stock__lte=F('stock_minimo'),
    ).order_by('stock_actual')[:10]
    
    # Importaciones pendientes
    importaciones_pendientes = Importaciones.objects.filter(
        estado__in=['True']
    ).order_by('fecha')[:5]
    
    # Ventas por tipo de producto (este mes)
    ventas_por_tipo = Detalle_Ventas.objects.filter(
        venta__fecha__gte=mes_actual,
        venta__estado__in=['True']
    ).values('producto__tipo').annotate(
        total=Sum(F('cantidad') * F('precio_unitario'))
    ).order_by('-total')
    
    # Clientes top
    clientes_top = Ventas.objects.filter(
        fecha__gte=hace_30_dias,
        estado__in=['True']
    ).values(
        'cliente__nombre',
        'cliente__tipo'
    ).annotate(
        total_compras=Sum('total'),
        num_compras=Count('id')
    ).order_by('-total_compras')[:5]
    
    # Ventas diarias últimos 30 días
    ventas_diarias = Venta.objects.filter(
        fecha__gte=hace_30_dias,
        estado__in=['PAGADO', 'PARCIAL']
    ).annotate(
        dia=TruncDate('fecha')
    ).values('dia').annotate(
        total=Sum('total'),
        cantidad=Count('id')
    ).order_by('dia')
    
    # Estadísticas generales
    total_productos = Producto.objects.filter(activo=True).count()
    total_clientes = Cliente.objects.filter(activo=True).count()
    total_proveedores = Proveedor.objects.filter(activo=True).count()
    
    # Margen de ganancia promedio
    margen_promedio = Producto.objects.filter(
        activo=True,
        precio_compra__gt=0
    ).annotate(
        margen=ExpressionWrapper(
            ((F('precio_venta') - F('precio_compra')) / F('precio_compra')) * 100,
            output_field=DecimalField()
        )
    ).aggregate(promedio=Avg('margen'))['promedio'] or 0
    
    context = {
        'total_ventas_mes': total_ventas_mes,
        'total_ventas_hoy': total_ventas_hoy,
        'productos_top': productos_top,
        'productos_bajo_stock': productos_bajo_stock,
        'importaciones_pendientes': importaciones_pendientes,
        'ventas_por_tipo': ventas_por_tipo,
        'clientes_top': clientes_top,
        'ventas_diarias': list(ventas_diarias),
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_proveedores': total_proveedores,
        'margen_promedio': round(margen_promedio, 2),
        'fecha_actual': hoy,
    }
    
    return render(request, 'dashboard/principal.html', context)


@login_required
def dashboard_inventario(request):
    
    # Productos por categoría
    productos_por_categoria = Producto.objects.filter(
        activo=True
    ).values(
        'tipo'
    ).annotate(
        cantidad=Count('id'),
        stock_total=Sum('stock_actual'),
        valor_inventario=Sum(F('stock_actual') * F('precio_compra'))
    ).order_by('-stock_total')
    
    # Productos que necesitan reorden
    productos_reorden = Producto.objects.filter(
        stock_actual__lte=F('stock_minimo'),
        activo=True
    ).select_related('proveedor').order_by('stock_actual')
    
    # Productos sin movimiento (últimos 30 días)
    hace_30_dias = timezone.now() - timedelta(days=30)
    productos_con_ventas = DetalleVenta.objects.filter(
        venta__fecha__gte=hace_30_dias
    ).values_list('producto_id', flat=True).distinct()
    
    productos_sin_movimiento = Producto.objects.filter(
        activo=True
    ).exclude(
        id__in=productos_con_ventas
    ).order_by('-stock_actual')[:20]
    
    # Valor total del inventario
    valor_total_inventario = Producto.objects.filter(
        activo=True
    ).aggregate(
        total=Sum(F('stock_actual') * F('precio_compra'))
    )['total'] or 0
    
    # Rotación de inventario por tipo
    rotacion_por_tipo = []
    for tipo_display in Producto.TIPOS_ALCOHOL:
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
    
    context = {
        'productos_por_categoria': productos_por_categoria,
        'productos_reorden': productos_reorden,
        'productos_sin_movimiento': productos_sin_movimiento,
        'valor_total_inventario': valor_total_inventario,
        'rotacion_por_tipo': rotacion_por_tipo,
    }
    
    return render(request, 'dashboard/inventario.html', context)


@login_required
def dashboard_ventas(request):
    
    # Parámetros de filtro
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if not fecha_inicio:
        fecha_inicio = (timezone.now() - timedelta(days=30)).date()
    else:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    
    if not fecha_fin:
        fecha_fin = timezone.now().date()
    else:
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    
    # Ventas en el período
    ventas = Venta.objects.filter(
        fecha__date__gte=fecha_inicio,
        fecha__date__lte=fecha_fin,
        estado__in=['PAGADO', 'PARCIAL']
    )
    
    # Métricas generales
    total_ventas = ventas.aggregate(Sum('total'))['total__sum'] or 0
    numero_ventas = ventas.count()
    ticket_promedio = total_ventas / numero_ventas if numero_ventas > 0 else 0
    
    # Ventas por vendedor
    ventas_por_vendedor = ventas.values(
        'vendedor__username',
        'vendedor__first_name',
        'vendedor__last_name'
    ).annotate(
        total=Sum('total'),
        cantidad=Count('id')
    ).order_by('-total')
    
    # Ventas por método de pago
    ventas_por_metodo = ventas.values('metodo_pago').annotate(
        total=Sum('total'),
        cantidad=Count('id')
    ).order_by('-total')
    
    # Ventas por tipo de cliente
    ventas_por_tipo_cliente = ventas.values(
        'cliente__tipo'
    ).annotate(
        total=Sum('total'),
        cantidad=Count('id')
    ).order_by('-total')
    
    # Evolución mensual
    ventas_mensuales = ventas.annotate(
        mes=TruncMonth('fecha')
    ).values('mes').annotate(
        total=Sum('total'),
        cantidad=Count('id')
    ).order_by('mes')
    
    # Productos más rentables
    productos_rentables = DetalleVenta.objects.filter(
        venta__fecha__date__gte=fecha_inicio,
        venta__fecha__date__lte=fecha_fin,
        venta__estado__in=['PAGADO', 'PARCIAL']
    ).values(
        'producto__nombre',
        'producto__marca'
    ).annotate(
        cantidad_vendida=Sum('cantidad'),
        ingresos=Sum(F('cantidad') * F('precio_unitario')),
        costo=Sum(F('cantidad') * F('producto__precio_compra')),
        ganancia=Sum(F('cantidad') * F('precio_unitario')) - Sum(F('cantidad') * F('producto__precio_compra'))
    ).order_by('-ganancia')[:10]
    
    context = {
        'total_ventas': total_ventas,
        'numero_ventas': numero_ventas,
        'ticket_promedio': ticket_promedio,
        'ventas_por_vendedor': ventas_por_vendedor,
        'ventas_por_metodo': ventas_por_metodo,
        'ventas_por_tipo_cliente': ventas_por_tipo_cliente,
        'ventas_mensuales': list(ventas_mensuales),
        'productos_rentables': productos_rentables,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    
    return render(request, 'dashboard/ventas.html', context)


@login_required
def dashboard_importaciones(request):
    
    
    # Importaciones por estado
    importaciones_por_estado = ImportacionLote.objects.values(
        'estado'
    ).annotate(
        cantidad=Count('id'),
        valor_total=Sum('costo_total')
    ).order_by('estado')
    
    # Próximas llegadas
    proximas_llegadas = ImportacionLote.objects.filter(
        estado__in=['PLANIFICADO', 'EN_TRANSITO', 'ADUANA'],
        fecha_estimada_llegada__gte=timezone.now().date()
    ).order_by('fecha_estimada_llegada')[:10]
    
    # Importaciones retrasadas
    importaciones_retrasadas = ImportacionLote.objects.filter(
        estado__in=['PLANIFICADO', 'EN_TRANSITO', 'ADUANA'],
        fecha_estimada_llegada__lt=timezone.now().date()
    ).order_by('fecha_estimada_llegada')
    
    # Proveedores más usados
    proveedores_top = ImportacionLote.objects.filter(
        fecha_orden__gte=timezone.now() - timedelta(days=180)
    ).values(
        'proveedor__nombre',
        'proveedor__pais_origen'
    ).annotate(
        num_lotes=Count('id'),
        valor_total=Sum('costo_total')
    ).order_by('-valor_total')[:10]
    
    # Costos promedio
    costos_promedio = ImportacionLote.objects.aggregate(
        costo_prom=Avg('costo_total'),
        envio_prom=Avg('costo_envio'),
        aduana_prom=Avg('costo_aduana')
    )
    
    context = {
        'importaciones_por_estado': importaciones_por_estado,
        'proximas_llegadas': proximas_llegadas,
        'importaciones_retrasadas': importaciones_retrasadas,
        'proveedores_top': proveedores_top,
        'costos_promedio': costos_promedio,
    }
    
    return render(request, 'dashboard/importaciones.html', context)
"""