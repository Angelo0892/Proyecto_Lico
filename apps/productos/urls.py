# urls.py
from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [

    # Clasificacion de Productos
    path('index_producto/', views.index_producto, name='index_producto'),
    path('producto/crear/', views.crear_producto, name='crear_producto'),
    path('producto/editar/<int:id>', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:id>', views.eliminar_producto, name='eliminar_producto'),

    # Clasificacion de Categorias
    path('index_categoria', views.index_categoria, name='index_categoria'),
    path('categoria/crear/', views.crear_categoria, name='crear_categoria'),
    path('categoria/editar/<int:id>', views.editar_categoria, name='editar_categoria'),
    path('categoria/eliminar/<int:id>', views.eliminar_categoria, name='eliminar_categoria')
]