# urls.py
from django.urls import path
from . import views
from .controls import inventario, categorias

app_name = 'dashboard'

urlpatterns = [
    path('', views.principal, name='principal'),
    path('ventas/', views.dashboard_ventas, name='ventas'),
    path('importaciones/', views.dashboard_importaciones, name='importaciones'),

    #Acceso a categorias
    #path('categorias/', categorias),

    #Acceso a inventario

    #path('inventario/', inventario.inventario, name='inventario'),
    #path('inventario/producto/guardar', inventario.guardar_producto, name='inventario.producto.guardar'),
    #path('inventario/producto/<int:id>', inventario.editar_producto, name='inventario.producto.editar'),
    #path('inventario/producto/<int:id>/eliminar/', inventario.eliminar_producto, name='inventario.producto.eliminar'),    
]