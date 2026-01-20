from django import forms
from ..models import Productos, Categorias, Ubicacion

class formulario_producto(forms.ModelForm):

    class Meta:
        model = Productos

        fields = [
            "nombre",
            "marca",
            "origen",
            "stock",
            "proveedor_id",
            "precio_unitario",
            "categoria_id",
            "ubicacion_id"
        ]

        labels = {
            "proveedor_id": "Proveedor",
            "categoria_id": "Categoria",
            "ubicacion_id": "Ubicacion",
            "nombre": "Nombre del producto",
            "marca": "Marca",
            "stock": "Stock",
            "origen": "Origen",
            "precio_unitario": "Precio Unitario"
        }

        widgets = {
            "nombre": forms.TextInput(attrs={"class": "input"}),
            "marca": forms.TextInput(attrs={"class": "input"}),
            "stock": forms.TextInput(attrs={"class": "input"}),
            "origen": forms.TextInput(attrs={"class": "input"}),
            "precio_unitario": forms.TextInput(attrs={"class": "input"}),
             
            "proveedor_id": forms.Select(attrs={"class": "input"}),
            "categoria_id": forms.Select(attrs={"class": "input"}),
            "ubicacion_id": forms.Select(attrs={"class": "input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        self.fields["categoria_id"].queryset = Categorias.objects.all()
        self.fields["ubicacion_id"].queryset = Ubicacion.objects.all() 
    