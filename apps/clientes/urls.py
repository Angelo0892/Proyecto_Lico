# urls.py
from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('clientes/index_cliente/', views.index_cliente, name='index_cliente'),
    path('clientes/crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar_cliente/<int:id>', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar_cliente/<int:id>', views.eliminar_cliente, name='eliminar_cliente'),
]