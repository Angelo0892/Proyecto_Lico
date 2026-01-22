# urls.py
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('index_proveedor/', views.index_proveedor, name='index_proveedor'),
]