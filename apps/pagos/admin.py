from django.contrib import admin
from .models import Pagos, Metodos_Pago, Detalle_Pagos

# Register your models here.

admin.site.register(Pagos)
admin.site.register(Metodos_Pago)
admin.site.register(Detalle_Pagos)
