from django import forms
from .models import Proveedores

class formulario_proveedor(forms.ModelForm):
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
        }

        widgets ={
            "nit": forms.TextInput(attrs={"class": "input"}),
            "nombre": forms.TextInput(attrs={"class": "input"}),
            "tipo_proveedor": forms.TextInput(attrs={"class": "input"}),
            "apellido1": forms.TextInput(attrs={"class": "input"}),
            "apellido2": forms.TextInput(attrs={"class": "input"}),
            "pais": forms.TextInput(attrs={"class": "input"}),
            "contacto": forms.TextInput(attrs={"class": "input"}),
            "telefono": forms.TextInput(attrs={"class": "input"}),
            "correo": forms.EmailInput(attrs={"class": "input"}),
        }