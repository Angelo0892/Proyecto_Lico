from django.db import models

class Clientes(models.Model):
    ci = models.CharField(max_length=20, null=True)
    nit = models.CharField(max_length=20, null=True)
    tipo_cliente = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50, null=True)
    apellido2 = models.CharField(max_length=50, null=True)
    direccion = models.CharField(max_length=200, null=True)
    telefono = models.CharField(max_length=30)
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre} {self.apellido1 or ''}"
