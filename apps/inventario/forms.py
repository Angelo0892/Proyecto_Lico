from django import forms
from .models import Proveedores

class formulario_proveedor():
    class Meta:

        model = Proveedores

        fields = [
            "nit",
            "nombre",
            "tipo_proveedor",
            "apellido1",
            "apellido2",
            "pais",
            "contacto",
            "telefono",
            "correo",
            "fecha_registro"
        ]

        labels = {
            "nit": "Numero de Identificacion Tributaria",
            "nombre": "Nombre de Proveedor",
            "tipo_proveedor": "Tipo de Proveedor",
            "apellido1": "Apellido Paterno",
            "apellido2": "Apellido Materno",
            "pais": "Pais de origen",
            "contacto": "Nombre de personal",
            "telefono": "Telefono o Celular",
            "correo": "Correo electronico",
            "fecha_registro": "Fecha de registro"
        }

        widgets ={
            
        }