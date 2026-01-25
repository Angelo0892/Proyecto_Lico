from django import forms
from .models import Clientes

class formulario_cliente(forms.ModelForm):

    class Meta:

        model = Clientes

        TIPO_CLIENTE_CHOICES = [
            ('minorista', 'Minorista'),
            ('mayorista', 'Mayorista'),
            ('restaurante', 'Restaurante'),
            ('bar', 'Bar'),
        ]

        fields = [
            "ci",
            "nit",
            "nombre",
            "tipo_cliente",
            "apellido1",
            "apellido2",
            "direccion",
            "telefono",
            "email",
        ]

        labels = {
            "ci": "Carnet de identidad",
            "nit": "Numero de identificacion tributaria",
            "tipo_cliente": "Tipo de cliente",
            "nombre": "Nombre",
            "apellido1": "Apellido Paterno",
            "apellido2": "Apellido Materno",
            "direccion": "Direccion",
            "telefono": "Telefono o celular",
            "email": "Correo Electronico",
        }

        tipo_cliente = forms.ChoiceField(
            choices=TIPO_CLIENTE_CHOICES,
            widget=forms.Select(attrs={"class": "form-select"})
        )

        widgets ={
            "ci": forms.TextInput(attrs={"class": "input"}),
            "nit": forms.TextInput(attrs={"class": "input"}),
            "nombre": forms.TextInput(attrs={"class": "input"}),
            "apellido1": forms.TextInput(attrs={"class": "input"}),
            "apellido2": forms.TextInput(attrs={"class": "input"}),
            "direccion": forms.TextInput(attrs={"class": "input"}),
            "telefono": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
        }