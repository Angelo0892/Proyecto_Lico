# urls.py
from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.index, name='index_productos'),
]