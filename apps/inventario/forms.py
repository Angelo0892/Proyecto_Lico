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
            "nit": forms.TextInput(attrs={"class": "input"}),
            "nombre": forms.TextInput(attrs={"class": "input"}),
            "tipo_proveedor": forms.TextInput(attrs={"Class": "input"}),
            "apellido1": forms.TextInput(attrs={"Class": "input"}),
            "apellido2": forms.TextInput(attrs={"Class": "input"}),
            "pais": forms.TextInput(attrs={"Class": "input"}),
            "contacto": forms.TextInput(attrs={"Class": "input"}),
            "telefono": forms.TextInput(attrs={"Class": "input"}),
            "correo": forms.EmailInput(attrs={"Class": "input"}),
            "fecha_registro": forms.TextInput(attrs={"Class": "input"}),
        }