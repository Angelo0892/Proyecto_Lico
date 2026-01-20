from django import forms
from ..models import Categorias

class formulario_categoria(forms.ModelForm):

    class Meta:

        model = Categorias

        fields = [
            "nombre",
            "descripcion",
        ]

        labels = {
            "nombre": "Categoria",
            "descripcion": "Descripcion",
        }

        widgets = {
            "nombre": forms.TextInput(attrs={"class": "input"}),
            "descripcion": forms.TextInput(attrs={"class": "input_text_tarea"},)
        }