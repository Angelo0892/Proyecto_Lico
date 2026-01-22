from django.shortcuts import render, redirect, get_object_or_404
from .models import Productos, Categorias, Ubicacion
from django.core.paginator import Paginator
from .forms import (
    formulario_producto, 
    formulario_categoria, 
    formulario_ubicacion
)

# Vistas de productos
def index_producto(request):

    lista_productos = Productos.objects.all().order_by("nombre")

    paginacion = Paginator(lista_productos, 10)
    numero_pagina = request.GET.get('page')
    productos = paginacion.get_page(numero_pagina)

    context = {
        "productos": productos,
    }

    return render(request, 'productos/index_producto.html', context)

def crear_producto(request):

    if request.method == 'POST':
        form = formulario_producto(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:index_producto")

    else:
        form = formulario_producto

    context = {
        "form": form
    }

    return render(request, "productos/crear_producto.html", context)

def editar_producto(request, id):
    producto = get_object_or_404(Productos, id = id)

    if request.method == 'POST':
        form = formulario_producto(request.POST, instance = producto)
        if form.is_valid():
            form.save()
            return redirect("productos:index_producto")
    else:
        form = formulario_producto(instance = producto)

    context = {
        "form": form
    }

    return render(request, "productos/editar_producto.html", context)

def eliminar_producto(request, id):
    producto = get_object_or_404(Productos, id = id)

    if request.method == 'POST':
        producto.delete()

    return redirect("productos:index_producto")

# Vistas de categoria 
def index_categoria(request):

    lista_categoria = Productos.objects.all().order_by("nombre")

    paginacion = Paginator(lista_categoria, 10)
    numero_pagina = request.GET.get('page')
    categorias = paginacion.get_page(numero_pagina)

    context = {
        "categorias": categorias,
    }

    return render(request, "categorias/index_categoria.html")

def crear_categoria(request):
    return 0

def editar_categoria(request):
    return 0

def eliminar_categoria(request):
    return 0