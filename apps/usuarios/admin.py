from django.contrib import admin
from .models import Usuarios, Roles, Permisos

# Register your models here.
admin.site.register(Usuarios)
admin.site.register(Roles)
admin.site.register(Permisos)
