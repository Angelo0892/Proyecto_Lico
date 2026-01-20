# urls.py
from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.index, name='index_clientes'),
]