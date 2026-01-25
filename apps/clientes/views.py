from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import formulario_cliente
from .models import Clientes

# Create your views here.
def index_cliente(request):

    query = request.GET.get('search', '')

    lista_clientes = Clientes.objects.all().order_by("nombre")

    if query:
        lista_clientes = lista_clientes.filter(
            Q(ci__icontains=query) |
            Q(nit__icontains=query) |
            Q(tipo_cliente__icontains=query) |
            Q(nombre__icontains=query) |
            Q(apellido1__icontains=query) |
            Q(apellido2__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query)
        )

    paginacion = Paginator(lista_clientes, 10)
    numero_pagina = request.GET.get('page')
    clientes = paginacion.get_page(numero_pagina)

    context = {
        "clientes": clientes
    }

    return render (request, "clientes/index_cliente.html", context)

def crear_cliente(request):
    if request.method == 'POST':
        form = formulario_cliente(request.POST)
        if form.is_valid():
            form.save()
            return redirect ("clientes:index_cliente")
    else:
        form = formulario_cliente()

    context = {
        "form": form
    }

    return render(request, "clientes/crear_cliente.html", context)

def editar_cliente(request, id):
    cliente = get_object_or_404(Clientes, id = id)

    if request.method == 'POST':
        form = formulario_cliente(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect ("clientes:index_cliente")
    else:
        form = formulario_cliente(instance=cliente)

    context = {
        "form": form
    }

    return render(request, "clientes/editar_cliente.html", context)

def eliminar_cliente(request, id):

    cliente = get_object_or_404(Clientes, id = id)

    if request.method == "POST":
        cliente.delete()

    return redirect("clientes:index_cliente")