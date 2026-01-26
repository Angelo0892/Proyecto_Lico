from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator 
from .models import Ventas, Detalle_Ventas, Productos


# Create your views here.
def index_venta(request):

    

    return 0

def buscar_producto(request):
    query = request.GET.get ('search', '')
    

    lista_productos = Productos.objects.all().order_by("nombre")

    if query:
        lista_productos = lista_productos.filter(
            Q(nombre__icontains=query) |
            Q(categoria_id__nombre__icontains=query) |
            Q(marca__icontains=query)
        )

    paginacion = Paginator(lista_productos, 10)
    numero_pagina = request.GET.get('page', 1)
    productos = paginacion.get_page(numero_pagina)

    html = render_to_string(
        'productos/parti'
    )
    
    return JsonResponse({'html': html})

def crear_venta(request):
    return 0