from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('about', views.contestame_telefonow)
]