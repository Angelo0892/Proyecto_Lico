from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta, datetime
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404

# --- FORMULARIOS ---
from .forms import (
    ClienteForm, ProductoForm, ImportacionForm, 
    ProveedorForm, UsuarioForm, RolForm, 
    VentaForm, DetalleVentaForm
)

# --- MODELOS ---
from .models import (
    Venta, DetalleVenta, Producto, Cliente, Proveedor,
    Importacion, DetalleImportacion, Categoria, 
    Factura, Usuario, Rol
)

@login_required
def principal(request):
    """ Función puente para redirigir al dashboard principal """
    return dashboard_principal(request)

@login_required
def dashboard_principal(request):
    """ Dashboard Operativo: Foco en Caja y Categorías """
    hoy = timezone.now().date()
    mes_actual = hoy.replace(day=1)
    
    # 1. KPI: Ventas
    ventas_mes = Venta.objects.filter(fecha__gte=mes_actual)
    total_ventas_mes = ventas_mes.aggregate(total=Sum('total'))['total'] or 0
    
    ventas_hoy = Venta.objects.filter(fecha__date=hoy)
    total_ventas_hoy = ventas_hoy.aggregate(total=Sum('total'))['total'] or 0
    
    # 2. KPI: Ganancia Estimada (Plata real, no %)
    # Calculamos: (Ventas Totales) - (Costo de esos productos)
    # Nota: Esto es un aproximado basado en el precio_compra actual del producto
    detalles_mes = DetalleVenta.objects.filter(venta__fecha__gte=mes_actual)
    costo_total = detalles_mes.aggregate(
        costo=Sum(F('cantidad') * F('producto__precio_compra'))
    )['costo'] or 0
    
    ganancia_estimada = total_ventas_mes - costo_total

    # 3. Top Productos (Se mantiene, es útil saber el "Rey" de ventas)
    productos_top = DetalleVenta.objects.filter(
        venta__fecha__gte=mes_actual
    ).values(
        'producto__nombre', 
        'producto__codigo',
        'producto__categoria__nombre'
    ).annotate(
        cantidad_vendida=Sum('cantidad'),
        ingresos=Sum('subtotal')
    ).order_by('-cantidad_vendida')[:5]
    
    # 4. Ventas por Categoría (NUEVO: Reemplaza a Clientes)
    # Esto te dice: "Vendiste 5000 en Ron, 2000 en Vinos..."
    ventas_por_categoria = DetalleVenta.objects.filter(
        venta__fecha__gte=mes_actual
    ).values('producto__categoria__nombre').annotate(
        total=Sum('subtotal')
    ).order_by('-total')[:5]

    # 5. Últimas Ventas (NUEVO: Reemplaza a Importaciones)
    # Monitor en tiempo real
    ultimas_ventas = Venta.objects.select_related('cliente', 'usuario').all().order_by('-fecha')[:5]
    
    # 6. Alertas de Stock (Se mantiene, es vital)
    productos_bajo_stock = Producto.objects.filter(
        stock_actual__lte=F('stock_minimo'), activo=True
    ).select_related('categoria').order_by('stock_actual')[:5]
    
    context = {
        'total_ventas_mes': total_ventas_mes,
        'total_ventas_hoy': total_ventas_hoy,
        'ganancia_estimada': ganancia_estimada, # <--- Enviamos Ganancia $
        'total_productos': Producto.objects.filter(activo=True).count(),
        
        'productos_top': productos_top,
        'ventas_por_categoria': ventas_por_categoria, # <--- Categorías
        'ultimas_ventas': ultimas_ventas,             # <--- Monitor en vivo
        'productos_bajo_stock': productos_bajo_stock,
        'fecha_actual': hoy,
    }
    
    return render(request, 'dashboard/principal.html', context)

@login_required
def dashboard_ventas(request):
    """ Vista detallada de Ventas """
    fecha_inicio = request.GET.get('fecha_inicio', (timezone.now() - timedelta(days=30)).date())
    fecha_fin = request.GET.get('fecha_fin', timezone.now().date())
    
    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

    ventas = Venta.objects.filter(
        fecha__date__gte=fecha_inicio,
        fecha__date__lte=fecha_fin
    )
    
    total_periodo = ventas.aggregate(Sum('total'))['total__sum'] or 0
    cantidad_ventas = ventas.count()
    
    ventas_cliente = ventas.values('cliente__nombre', 'cliente__apellido1').annotate(
        total=Sum('total'),
        cantidad=Count('id')
    ).order_by('-total')[:10]

    ventas_diarias = ventas.annotate(
        dia=TruncDate('fecha')
    ).values('dia').annotate(
        total=Sum('total')
    ).order_by('dia')

    context = {
        'ventas': ventas[:50],
        'total_periodo': total_periodo,
        'cantidad_ventas': cantidad_ventas,
        'ventas_cliente': ventas_cliente,
        'ventas_diarias': list(ventas_diarias),
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'dashboard/ventas.html', context)

@login_required
def dashboard_inventario(request):
    """ Vista de Inventario """
    productos = Producto.objects.filter(activo=True).select_related('categoria', 'proveedor')
    
    valor_inventario = productos.aggregate(
        valor=Sum(F('stock_actual') * F('precio_compra'))
    )['valor'] or 0
    
    por_categoria = productos.values('categoria__nombre').annotate(
        cantidad=Count('id'),
        stock=Sum('stock_actual')
    ).order_by('-stock')
    
    context = {
        'productos': productos,
        'valor_inventario': valor_inventario,
        'por_categoria': por_categoria
    }
    return render(request, 'dashboard/inventario.html', context)

@login_required
def dashboard_importaciones(request):
    """ Vista de Importaciones """
    importaciones = Importacion.objects.all().order_by('-fecha_pedido')
    
    por_estado = importaciones.values('estado').annotate(
        cantidad=Count('id'),
        total=Sum('total')
    )
    
    context = {
        'importaciones': importaciones,
        'por_estado': por_estado
    }
    return render(request, 'dashboard/importaciones.html', context)

# --- VISTAS DE CREACIÓN ---

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:clientes')
    else:
        form = ClienteForm()
    return render(request, 'dashboard/form_cliente.html', {'form': form})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:inventario')
    else:
        form = ProductoForm()
    return render(request, 'dashboard/form_producto.html', {'form': form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        # instance=producto es la clave: carga los datos existentes
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('dashboard:inventario')
    else:
        form = ProductoForm(instance=producto)
    
    # Reutilizamos el mismo formulario de crear
    return render(request, 'dashboard/form_producto.html', {
        'form': form, 
        'titulo': f'Editar Producto: {producto.nombre}'
    })

@login_required
def crear_importacion(request):
    if request.method == 'POST':
        form = ImportacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:importaciones')
    else:
        form = ImportacionForm()
    return render(request, 'dashboard/form_importacion.html', {'form': form})

@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'dashboard/form_proveedor.html', {'form': form})

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'dashboard/form_usuario.html', {'form': form})

@login_required
def crear_rol(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:usuarios')
    else:
        form = RolForm()
    return render(request, 'dashboard/form_usuario.html', {'form': form, 'es_rol': True})

@login_required
def crear_venta(request):
    # CAMBIO: extra=1 (Empieza con una sola fila vacía, no 3)
    DetalleVentaFormSet = inlineformset_factory(
        Venta, DetalleVenta, form=DetalleVentaForm,
        extra=1, can_delete=True
    )

    if request.method == 'POST':
        form = VentaForm(request.POST)
        formset = DetalleVentaFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            venta = form.save(commit=False)
            
            # Asignación automática de empleado
            empleado = Usuario.objects.filter(activo=True).first()
            if empleado:
                venta.usuario = empleado
                venta.save()
            else:
                return render(request, 'dashboard/form_venta.html', {
                    'form': form, 'formset': formset,
                    'error_mensaje': 'Error: No hay empleados activos.'
                })
            
            detalles = formset.save(commit=False)
            total_venta = 0

            for detalle in detalles:
                # Si no seleccionó producto (fila vacía), continuar
                if not detalle.producto:
                    continue

                producto = detalle.producto
                detalle.venta = venta
                detalle.precio_unitario = producto.precio_venta
                detalle.subtotal = detalle.cantidad * producto.precio_venta
                
                detalle.save()
                total_venta += detalle.subtotal

                # Descontar stock
                producto.stock_actual -= detalle.cantidad
                producto.save()

            venta.total = total_venta
            venta.save()

            return redirect('dashboard:ventas')
    else:
        form = VentaForm()
        formset = DetalleVentaFormSet()

    return render(request, 'dashboard/form_venta.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Registrar Nueva Venta'
    })

# --- NUEVA FUNCIÓN PARA EDITAR ---
@login_required
def editar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    
    # extra=0 porque NO queremos filas vacías automáticas al editar
    DetalleVentaFormSet = inlineformset_factory(
        Venta, DetalleVenta, form=DetalleVentaForm,
        extra=0, can_delete=True
    )

    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        formset = DetalleVentaFormSet(request.POST, instance=venta)

        if form.is_valid() and formset.is_valid():
            venta = form.save() # Guarda cabecera
            
            # Guardamos los formsets (incluye eliminados si marcaste delete)
            detalles = formset.save(commit=False)
            
            # Nota: Al editar es complejo recalcular stock si cambian cantidades.
            # Por simplicidad ahora solo guardamos montos.
            total_venta = 0
            
            # 1. Procesar objetos borrados
            for obj in formset.deleted_objects:
                # Devolver stock si se borra
                obj.producto.stock_actual += obj.cantidad
                obj.producto.save()
                obj.delete()

            # 2. Procesar objetos nuevos/editados
            for detalle in detalles:
                producto = detalle.producto
                detalle.venta = venta
                detalle.precio_unitario = producto.precio_venta
                detalle.subtotal = detalle.cantidad * producto.precio_venta
                detalle.save()
                total_venta += detalle.subtotal
                
                # (Aquí faltaría lógica avanzada de ajuste de stock al editar, 
                # pero por ahora dejémoslo funcional en guardar precios)

            venta.total = total_venta
            venta.save()

            return redirect('dashboard:ventas')
    else:
        form = VentaForm(instance=venta)
        formset = DetalleVentaFormSet(instance=venta)

    return render(request, 'dashboard/form_venta.html', {
        'form': form,
        'formset': formset,
        'titulo': f'Editar Venta #{venta.id}'
    })

# --- VISTAS DE LISTADOS (Tablas) ---

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'dashboard/lista_clientes.html', {'datos': clientes})

@login_required
def lista_proveedores(request):
    proveedores = Proveedor.objects.all().order_by('-id')
    return render(request, 'dashboard/lista_proveedores.html', {'datos': proveedores})

@login_required
def lista_facturas(request):
    # Traemos facturas con datos de cliente
    facturas = Factura.objects.select_related('venta__cliente').all().order_by('-fecha_emision')

    # KPIs rápidos
    mes_actual = timezone.now().date().replace(day=1)
    
    total_mes = facturas.filter(
        fecha_emision__gte=mes_actual, 
        estado=True 
    ).aggregate(Sum('monto_total'))['monto_total__sum'] or 0

    cantidad_anuladas = facturas.filter(estado=False).count()

    context = {
        'datos': facturas,
        'total_mes': total_mes,
        'anuladas': cantidad_anuladas
    }
    return render(request, 'dashboard/lista_facturas.html', context)

@login_required
def lista_usuarios(request):
    # Traemos usuarios y roles
    usuarios = Usuario.objects.select_related('rol').all()
    roles = Rol.objects.all()
    
    context = {
        'datos': usuarios,
        'roles': roles
    }
    return render(request, 'dashboard/lista_usuarios.html', context)