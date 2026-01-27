import pdfkit
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta, datetime
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from decimal import Decimal
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction

# --- FORMULARIOS ---
from .forms import (
    ClienteForm, ProductoForm, ImportacionForm, 
    ProveedorForm, UsuarioForm, RolForm, 
    VentaForm, DetalleVentaForm,
    CategoriaForm
)

# --- MODELOS ---
from .models import (
    Venta, DetalleVenta, Producto, Cliente, Proveedor,
    Importacion, DetalleImportacion, Categoria, 
    Factura, Usuario, Rol, MetodoPago, Pago, DetallePago
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

# --- VISTAS DE Clientes ---

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
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('dashboard:clientes')
    else:
        form = ClienteForm(instance=cliente)
    
    # Reutilizamos el mismo formulario de crear
    return render(request, 'dashboard/form_cliente.html', {'form': form})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        cliente.delete()

    return redirect ('dashboard:clientes')

# --- VISTA DE PRODUCTOS ---

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

# --- VISTA DE Categorias ---

@login_required
def crear_categoria(request):
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:categorias')
    else:
        form = CategoriaForm()
    return render(request, 'dashboard/form_categoria.html', {'form': form})

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        # instance=producto es la clave: carga los datos existentes
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('dashboard:categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    # Reutilizamos el mismo formulario de crear
    return render(request, 'dashboard/form_categoria.html', {
        'form': form, 
        'titulo': f'Editar Categoria: {categoria.nombre}'
    })

@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        categoria.delete()
    
    # Reutilizamos el mismo formulario de crear
    return redirect('dashboard:categorias')


# --- VISTA DE Importaciones ---

@login_required
def crear_importacion(request):
    proveedores = Proveedor.objects.all()
    return render(request, "dashboard/form_importacion.html", {
        "proveedores": proveedores
    })


@login_required
def buscar_productos_importacion(request):
    q = request.GET.get("q", "")
    productos = Producto.objects.filter(nombre__icontains=q, activo=True)

    data = []
    for p in productos:
        data.append({
            "id": p.id,
            "nombre": p.nombre,
            "codigo": p.codigo,
            "proveedor": p.proveedor.nombre if p.proveedor else "",
            "precio_compra": float(p.precio_compra),
            "stock": p.stock_actual,
        })
    return JsonResponse(data, safe=False)


@login_required
@transaction.atomic
def guardar_importacion(request):
    if request.method == "POST":
        importacion = Importacion.objects.create(
            proveedor_id=request.POST["proveedor_id"],
            fecha_pedido=request.POST["fecha_pedido"],
            fecha_llegada=request.POST.get("fecha_llegada") or None,
            estado=request.POST["estado"],
            total=request.POST["total"]
        )

        for i in range(len(request.POST.getlist("producto_id[]"))):
            DetalleImportacion.objects.create(
                importacion=importacion,
                producto_id=request.POST.getlist("producto_id[]")[i],
                cantidad=request.POST.getlist("cantidad[]")[i],
                costo_unitario=request.POST.getlist("precio[]")[i],
            )

        return redirect("dashboard:importaciones")   

@transaction.atomic
def ingresar_stock_importacion(importacion):
    if importacion.stock_ingresado:
        return  # ⚠️ Evita doble ingreso

    for detalle in importacion.detalleimportacion_set.all():
        producto = detalle.producto
        producto.stock_actual += detalle.cantidad
        producto.precio_compra = detalle.costo_unitario  # opcional
        producto.save()

    importacion.stock_ingresado = True
    importacion.estado = "RECIBIDO"
    importacion.save()

@login_required
def recibir_importacion(request, pk):
    importacion = get_object_or_404(Importacion, pk=pk)

    if importacion.estado == "RECIBIDO":
        return redirect("dashboard:importaciones")

    ingresar_stock_importacion(importacion)

    messages.success(request, "Stock ingresado correctamente.")
    return redirect("dashboard:importaciones")

# --- Vista de proveedores ---
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
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        # instance=producto es la clave: carga los datos existentes
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('dashboard:proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    
    # Reutilizamos el mismo formulario de crear
    return render(request, 'dashboard/form_proveedor.html', {
        'form': form, 
        'titulo': f'Editar Producto: {proveedor.nombre}'
    })

@login_required
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk = pk)

    if request.method == 'POST':
        proveedor.delete()

    return redirect('dashboard:proveedores')


# --- Vistas de usuarios ---
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

# --- Funciones para la venta ---
@login_required
def crear_venta(request):
    """Vista principal para crear la venta"""
    productos_list = Producto.objects.all().order_by("nombre")
    paginator = Paginator(productos_list, 10)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)

    return render(request, "dashboard/form_venta.html", {
        "productos": productos,
    })

@login_required
def guardar_venta(request):
    if request.method != "POST":
        return redirect("dashboard:crear_venta")

    cliente = Cliente.objects.get(id=request.POST.get("cliente_id"))
    usuario = request.user
    total = Decimal(request.POST.get("total"))

    venta = Venta.objects.create(
        cliente=cliente,
        usuario=usuario,
        total=total,
        estado="PAGADO"
    )

    productos = request.POST.getlist("producto_id[]")
    cantidades = request.POST.getlist("cantidad[]")
    precios = request.POST.getlist("precio[]")

    for i in range(len(productos)):
        producto = Producto.objects.get(id=productos[i])
        cantidad = int(cantidades[i])
        precio = Decimal(precios[i])
        subtotal = cantidad * precio

        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio,
            subtotal=subtotal
        )

        producto.stock_actual -= cantidad
        producto.save()

    factura = Factura.objects.create(
        venta=venta,
        numero_factura=f"FAC-{venta.id:06d}",
        nit_cliente=cliente.nit,
        monto_total=total
    )

    metodo_pago = MetodoPago.objects.filter(
        id=request.POST.get("metodo_pago")
    ).first()

    if not metodo_pago:
        return redirect("dashboard:crear_venta")

    pago = Pago.objects.create(
        factura=factura,
        monto=total,
        metodo_pago=metodo_pago,
        referencia=request.POST.get("referencia")
    )

    DetallePago.objects.create(
        pago=pago,
        descripcion=f"Pago venta #{venta.id}",
        monto=total
    )

    return redirect("dashboard:ventas")


@login_required
def resumen_confirmar_venta(request):
    if request.method != "POST":
        return redirect("dashboard:crear_venta")

    cliente = Cliente.objects.get(id=request.POST.get("cliente_id"))

    productos = request.POST.getlist("producto_id[]")
    cantidades = request.POST.getlist("cantidad[]")
    precios = request.POST.getlist("precio[]")

    detalle = []
    total = Decimal("0")

    for i in range(len(productos)):
        producto = Producto.objects.get(id=productos[i])
        cantidad = int(cantidades[i])
        precio = Decimal(precios[i])
        subtotal = cantidad * precio
        total += subtotal

        detalle.append({
            "producto": producto,
            "producto_id": producto.id,
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": subtotal
        })

    return render(request, "dashboard/confirmar_venta.html", {
        "cliente": cliente,
        "detalle": detalle,
        "total": total,
        "metodos_pago": MetodoPago.objects.all()
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

# --- Vista facturas ---

@login_required
def detalle_factura(request, pk):
    """
    Muestra la factura en detalle y permite actualizar su estado (válida o no).
    """
    factura = get_object_or_404(Factura, pk=pk)

    if request.method == "POST":
        # Cambiar estado de la factura
        nuevo_estado = request.POST.get("estado") == "True"
        factura.estado = nuevo_estado
        factura.save()
        messages.success(request, f"Estado de la factura #{factura.numero_factura} actualizado.")
        return redirect("dashboard:facturacion")

    return render(request, "dashboard/detalle_factura.html", {"factura": factura})


# --- Creacion de factura en pdf en proceso --- 
@login_required
def factura_pdf(request, pk):
    """
    Genera la factura en PDF y permite descargarla usando PDFKit.
    """
    # Obtener la factura
    factura = get_object_or_404(Factura, pk=pk)

    # Renderizar la plantilla HTML con los datos de la factura
    html_string = render_to_string("dashboard/factura_pdf.html", {"factura": factura})

    # Configuración opcional para wkhtmltopdf (puedes ajustar la ruta en Windows)
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'no-outline': None,
    }

    # Generar PDF desde la plantilla HTML
    pdf = pdfkit.from_string(html_string, False, options=options)

    # Crear respuesta HTTP para descarga
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=factura_{factura.numero_factura}.pdf'
    return response

# --- VISTAS DE LISTADOS (Tablas) ---

@login_required
def lista_clientes(request):
    search = request.GET.get ('search', '')

    datos = Cliente.objects.all().order_by("nombre")

    if search:
        datos = datos.filter(
            Q(ci__icontains=search) |
            Q(nit__icontains=search) |
            Q(tipo_cliente__icontains=search) |
            Q(nombre__icontains=search) |
            Q(apellido1__icontains=search) |
            Q(apellido2__icontains=search) |
            Q(direccion__icontains=search) |
            Q(telefono__icontains=search) |
            Q(email__icontains=search)
        )

    paginacion = Paginator(datos, 10)
    numero_pagina = request.GET.get('page')
    datos = paginacion.get_page(numero_pagina)

    context = {
        "datos": datos,
        "search": search,
    }
    return render(request, 'dashboard/lista_clientes.html', context)

@login_required
def lista_proveedores(request):
    search = request.GET.get('search', '')

    datos = Proveedor.objects.all().order_by("nombre")

    if search:
        datos = datos.filter(
            Q(nombre__icontains=search) |
            Q(tipo_proveedor__icontains=search) |
            Q(contacto__icontains=search) |
            Q(telefono__icontains=search) |
            Q(email__icontains=search) |
            Q(direccion__icontains=search) |
            Q(pais__icontains=search)
        )

    paginacion = Paginator(datos, 10)
    numero_pagina = request.GET.get('page')
    datos = paginacion.get_page(numero_pagina)

    context = {
        'datos': datos,
        'search': search
    }

    return render(request, 'dashboard/lista_proveedores.html', context)

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

@login_required
def lista_productos(request):
    
    search = request.GET.get ('search', '')

    datos = Producto.objects.all().order_by("nombre")

    if search:
        datos = datos.filter(
            Q(nombre__icontains=search) |
            Q(categoria_id__nombre__icontains=search) |
            Q(marca__icontains=search)
        )

    paginacion = Paginator(datos, 10)
    numero_pagina = request.GET.get('page')
    datos = paginacion.get_page(numero_pagina)

    context = {
        "datos": datos,
        "search": search,
    }

    return render(request, 'dashboard/lista_producto.html', context)

@login_required
def lista_categorias(request):
    
    search = request.GET.get ('search', '')

    datos = Categoria.objects.all().order_by("nombre")

    if search:
        datos = datos.filter(
            Q(nombre__icontains=search) |
            Q(descripcion__icontains=search)
        )

    paginacion = Paginator(datos, 10)
    numero_pagina = request.GET.get('page')
    datos = paginacion.get_page(numero_pagina)

    context = {
        "datos": datos,
        "search": search,
    }

    return render(request, 'dashboard/lista_categorias.html', context)

@login_required
def buscar_clientes(request):
    q = request.GET.get('q', '')
    clientes = Cliente.objects.filter(
        Q(nombre__icontains=q) | Q(ci__icontains=q) | Q(nit__icontains=q)
    ).values('id','nombre','ci','nit')[:10]
    return JsonResponse(list(clientes), safe=False)

# ===================================================
# BUSCADOR PRODUCTOS AJAX
# ===================================================
@login_required
def lista_venta_productos(request):
    """Vista principal de venta"""
    productos = Producto.objects.all().order_by("nombre")
    return render(request, "dashboard/form_venta.html", {"productos": productos})

@login_required
def buscar_productos_ajax(request):
    query = request.GET.get("q", "")
    page = request.GET.get("page", 1)

    productos = Producto.objects.all().order_by("nombre")
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(codigo__icontains=query)
        )

    paginador = Paginator(productos, 5)
    productos_page = paginador.get_page(page)

    html = render_to_string(
        "dashboard/partials/productos_table_rows.html",
        {"productos": productos_page}
    )

    data = {
        "html": html,
        "num_pages": paginador.num_pages,
        "current_page": productos_page.number,
    }
    return JsonResponse(data)