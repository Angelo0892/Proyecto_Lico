from django.contrib import admin
from .models import Detalle_Importaciones, Importaciones, Proveedores

# Register your models here.
admin.site.register(Proveedores)
admin.site.register(Importaciones)
admin.site.register(Detalle_Importaciones)
