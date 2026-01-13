# urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_principal, name='principal'),
    path('inventario/', views.dashboard_inventario, name='inventario'),
    path('ventas/', views.dashboard_ventas, name='ventas'),
    path('importaciones/', views.dashboard_importaciones, name='importaciones'),
]