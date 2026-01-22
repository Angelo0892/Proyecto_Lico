from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Productos, Categorias, Ubicacion
from django.core.paginator import Paginator
from .forms import (
    formulario_producto, 
    formulario_categoria, 
    formulario_ubicacion
)

# Vistas de productos
def index_producto(request):

    query = request.GET.get ('search', '')

    lista_productos = Productos.objects.all().order_by("nombre")

    if query:
        lista_productos = lista_productos.filter(
            Q(nombre__icontains=query) |
            Q(categoria_id__nombre__icontains=query) |
            Q(marca__icontains=query)
        )

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

    query = request.GET.get ('search', '')

    lista_categoria = Categorias.objects.all().order_by("nombre")

    if query:
        lista_categoria = lista_categoria.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )

    paginacion = Paginator(lista_categoria, 10)
    numero_pagina = request.GET.get('page')
    categorias = paginacion.get_page(numero_pagina)

    context = {
        "categorias": categorias,
    }

    return render(request, "categorias/index_categoria.html", context)

def crear_categoria(request):

    if request.method == 'POST':
        form = formulario_categoria(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:index_categoria")

    else:
        form = formulario_categoria()

    context = {
        "form": form
    }

    return render(request, "categorias/crear_categoria.html", context)

def editar_categoria(request, id):

    categoria = get_object_or_404(Categorias, id = id)

    if request.method == 'POST':
        form = formulario_categoria(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("productos:index_categoria")

    else:
        form = formulario_categoria(instance=categoria)

    context = {
        "form": form
    }

    return render(request, "categorias/editar_categoria.html", context)

def eliminar_categoria(request, id):

    categoria = get_object_or_404(Categorias, id = id)

    if request.method == 'POST':
        categoria.delete()

    return redirect("productos:index_categoria")