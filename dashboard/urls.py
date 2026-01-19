# urls.py
from django.urls import path
from . import views
from .controls import inventario

app_name = 'dashboard'

urlpatterns = [
    path('', views.principal, name='principal'),

    #Acceso a inventario
    path('inventario/', inventario.inventario, name='inventario'),
    path('inventario/producto/<int:id>', inventario.producto, name='inventario.producto'),
    path('inventario/producto/<int:id>/eliminar/', inventario.eliminar_producto, name='inventario.producto.eliminar'),
    path('inventario/producto/<int:id>/actualizar', inventario.actualizar_producto, name='inventario.producto.actualizar')

    #path('ventas/', views.dashboard_ventas, name='ventas'),
    #path('importaciones/', views.dashboard_importaciones, name='importaciones'),
    
]