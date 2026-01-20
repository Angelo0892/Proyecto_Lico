from django.shortcuts import render

# Create your views here.

"""

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
    
    context = {
        'productos': productos,
        'valor_total_inventario': valor_total_inventario,
        'productos_reorden': productos_reorden,
        'productos_sin_movimiento': productos_sin_movimiento,
        #'rotacion_por_tipo': rotacion_por_tipo,
    }

    return render(request, 'dashboard/inventario/inventario.html', context)

@login_required
def guardar_producto(request):

    if request.method == 'POST':
        form = productos.formulario_producto(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:inventario')

    form = productos.formulario_producto()

    context = {
        'form': form,
    }

    return render(request, 'dashboard/inventario/producto_guardar.html', context)

@login_required
def editar_producto(request, id):

    producto = get_object_or_404(Productos, id = id)

    if request.method == 'POST':
        form = productos.formulario_producto(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('dashboard:inventario')
    else:
        form = productos.formulario_producto(instance=producto)

    context = {
        'producto': producto,
        'form': form,
    }

    return render(request, 'dashboard/inventario/producto_actualizar.html', context)

@login_required
def eliminar_producto(request, id):
    
    producto = get_object_or_404(Productos, id = id)

    if request.method == 'POST':
        producto.delete()
    else:
        print("Error al eliminar")

    return redirect('dashboard:inventario')

@login_required
def index_categorias(request):
    categorias_tabla = Categorias.objects.all()

    context = {
        'categorias_tabla': categorias_tabla
    }

    return render(request, 'dashboard/categoria/index_categoria.html', context)

@login_required
def guardar_categoria(request):
    if request.method == 'POST':
        form = categorias.formulario_categoria(request.POST)

        if form.is_valid():
            form.save()
            return redirect("") #Colocar direccion
    else:
        form = categorias.formulario_categoria()

    context = {
        "form": form,
    }

    return render(request, "dashboard/categoria/categoria_gardar", context)

@login_required
def editar_categoria(request, id):

    categoria = get_object_or_404(Categorias, id = id)

    if request.method == 'POST':
        form = categorias.formulario_categoria(request.POST, instance=categoria)

        if form.is_valid():
            return redirect("") #realizar
            
"""