# urls.py
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    #Proveedores
    path('index_proveedor/', views.index_proveedor, name='index_proveedor'),
    path('proveedor/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedor/editar/<int:id>', views.editar_proveedor, name='editar_proveedor'),
    path('proveedor/eliminar/<int:id>', views.eliminar_proveedor, name='eliminar_proveedor'),

    
]