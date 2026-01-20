# urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.principal, name='principal'),
    path('ventas/', views.dashboard_ventas, name='ventas'),
    path('importaciones/', views.dashboard_importaciones, name='importaciones'),

    #Acceso a categorias
    #path('categorias/', categorias),

    #Acceso a inventario
]