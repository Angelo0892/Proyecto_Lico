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
    path('productos/', views.lista_productos, name='productos'),
    path('categorias/', views.lista_categorias, name='categorias'),

    path('crear/usuario/', views.crear_usuario, name='crear_usuario'),
    path('crear/rol/', views.crear_rol, name='crear_rol'),
    
    # --- FORMULARIOS DE CREACIÓN ---
    path('crear/cliente/', views.crear_cliente, name='crear_cliente'),
    path('crear/producto/', views.crear_producto, name='crear_producto'),
    path('crear/importacion/', views.crear_importacion, name='crear_importacion'),
    path('crear/proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('crear/venta/', views.crear_venta, name='crear_venta'),
    path('crear/categoria/', views.crear_categoria, name = 'crear_categoria'),
    
    # --- Formularios de Edicion ---
    path('editar/venta/<int:pk>/', views.editar_venta, name='editar_venta'),
    path('editar/categoria/<int:pk>/', views.editar_categoria, name = 'editar_categoria'),
    path('editar/producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('editar/proveedor/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('editar/cliente/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    
    # --- Direcciones de eliminacion ---
    path('eliminar/categoria/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('eliminar/proveedor/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('eliminar/cliente/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # --- Direcciones para busqueda a tiempo real ---
    path('buscar/clientes/', views.buscar_clientes, name='buscar_clientes'),
    path('buscar_productos_ajax/', views.buscar_productos_ajax, name='buscar_productos_ajax'),
    path('confirmar_venta/', views.resumen_confirmar_venta, name='confirmar_venta'),
    path('guardar_venta/', views.guardar_venta, name='guardar_venta'),
]