from django.contrib import admin
from .models import Ventas, Facturas, Devoluciones, Detalle_Ventas, Detalle_Devoluciones

# Register your models here.

admin.site.register(Ventas)
admin.site.register(Facturas)
admin.site.register(Devoluciones)
admin.site.register(Detalle_Ventas)
admin.site.register(Detalle_Devoluciones)