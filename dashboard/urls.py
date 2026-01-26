from django.urls import path
from . import views

app_name = 'dashboard'  # <--- ESTO ES CRUCIAL para que funcione tu base.html

urlpatterns = [
    # --- RUTAS PRINCIPALES ---
    path('', views.principal, name='principal'),
    path('ventas/', views.dashboard_ventas, name='ventas'),
    path('inventario/', views.dashboard_inventario, name='inventario'),
    path('importaciones/', views.dashboard_importaciones, name='importaciones'),

    # --- NUEVAS SECCIONES (Según tu Base de Datos) ---
    path('clientes/', views.lista_clientes, name='clientes'),        # Tabla Clientes
    path('proveedores/', views.lista_proveedores, name='proveedores'), # Tabla Proveedores
    path('facturacion/', views.lista_facturas, name='facturacion'),    # Tablas Facturas/Pagos
    path('usuarios/', views.lista_usuarios, name='usuarios'),          # Tablas Usuarios/Roles
    path('crear/usuario/', views.crear_usuario, name='crear_usuario'),
    path('crear/rol/', views.crear_rol, name='crear_rol'),
    
    # --- FORMULARIOS DE CREACIÓN ---
    path('crear/cliente/', views.crear_cliente, name='crear_cliente'),
    path('crear/producto/', views.crear_producto, name='crear_producto'),
    path('crear/importacion/', views.crear_importacion, name='crear_importacion'),
    path('crear/proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('crear/venta/', views.crear_venta, name='crear_venta'),
    path('editar/venta/<int:pk>/', views.editar_venta, name='editar_venta'),
    path('editar/producto/<int:pk>/', views.editar_producto, name='editar_producto'),
]