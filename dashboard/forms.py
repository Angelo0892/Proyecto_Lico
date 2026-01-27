from django import forms
from .models import (
    Cliente, Producto, Importacion, Proveedor, 
    Usuario, Rol, Venta, DetalleVenta, Categoria
)

# 1. FORMULARIO DE CLIENTES
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido1', 'apellido2', 'ci', 'nit', 'telefono', 'email', 'direccion', 'tipo_cliente']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan'}),
            'apellido1': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido2': forms.TextInput(attrs={'class': 'form-control'}),
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tipo_cliente': forms.Select(attrs={'class': 'form-select'}),
        }

# 2. FORMULARIO DE PRODUCTOS
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo', 'marca', 'tipo', 'precio_compra', 'precio_venta', 'stock_minimo', 'categoria', 'proveedor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}), # O Select si defines choices
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
        }

# 3. FORMULARIO DE IMPORTACIONES (Cabecera)
class ImportacionForm(forms.ModelForm):
    class Meta:
        model = Importacion
        fields = ['proveedor', 'fecha_pedido', 'fecha_llegada', 'estado', 'observacion']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'fecha_pedido': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_llegada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'tipo_proveedor', 'contacto', 'telefono', 'email', 'direccion', 'pais']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_proveedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Distribuidor Oficial, Fabricante...'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Persona de contacto'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'rol', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        # IMPORTANTE: Aquí debe estar 'estado' para que se vea en pantalla
        fields = ['cliente', 'estado', 'observacion'] 
        
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select select-cliente'}),
            # Esto le da estilo al menú desplegable
            'estado': forms.Select(attrs={'class': 'form-select fw-bold', 'style': 'background-color: #f8f9fa;'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Notas...'}),
        }

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
        }
    
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

