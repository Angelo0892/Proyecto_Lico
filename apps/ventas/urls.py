# urls.py
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.index, name='index_ventas'),
]