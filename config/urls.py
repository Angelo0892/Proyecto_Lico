from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')), # Esto conecta tu app dashboard

    path('clientes/', include(('apps.clientes.urls', 'clientes'), namespace='clientes')),
    path('inventario/', include(('apps.inventario.urls', 'inventario'), namespace='inventario') ),
    path('pagos/', include(('apps.pagos.urls', 'pagos'), namespace = 'pagos')),
    path('productos/', include(('apps.productos.urls', 'productos'), namespace='productos')),
    path('usuarios/', include(('apps.usuarios.urls', 'usuarios'), namespace = 'usuarios')),
    path('ventas/', include(('apps.ventas.urls', 'ventas'), namespace='ventas')),
]