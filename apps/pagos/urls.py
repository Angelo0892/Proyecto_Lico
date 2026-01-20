# urls.py
from django.urls import path
from . import views

app_name = 'pagos'

urlpatterns = [
    path('', views.index, name='index_pagos'),
]