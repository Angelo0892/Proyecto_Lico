# urls.py
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('ventas/index_venta', views.index_venta, name='index_venta'),
    path('ventas/crear_venta', views.crear_venta, name='crear_venta')
]