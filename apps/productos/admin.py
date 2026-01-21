from django.contrib import admin
from .models import Productos, Categorias, Ubicacion

# Register your models here.

admin.site.register(Productos)
admin.site.register(Categorias)
admin.site.register(Ubicacion)