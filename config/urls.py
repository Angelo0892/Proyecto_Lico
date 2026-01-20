from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')), # Esto conecta tu app dashboard

    path('', include('apps.clientes.urls')),
    path('', include('apps.inventario.urls')),
    path('', include('apps.pagos.urls')),
    path('', include('apps.productos.urls')),
    path('', include('apps.usuarios.urls')),
    path('', include('apps.ventas.urls')),
]