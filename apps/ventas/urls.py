# urls.py
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.index_venta, name='index_ventas'),
]