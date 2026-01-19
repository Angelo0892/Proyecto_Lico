from django import forms

class crear_producto():
    nombre = forms.CharField(label="Nombre", max_length=80)
    marca = forms.CharField(label="Marca", max_length=50)
    origen = forms.CharField(label="Origen", max_length=50)
    stock = forms.IntegerField(label="Total de Stock")
    precio_unitario = forms.DecimalField(label="Precio unitario")
    