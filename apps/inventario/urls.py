# urls.py
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.index, name='index_inventario'),
]