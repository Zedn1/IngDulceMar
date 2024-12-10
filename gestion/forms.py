from django import forms
from django.forms import modelformset_factory
from .models import Pedido, DetallePedido, Producto

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'estado']  # Incluye los campos necesarios

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')

        if not producto or not cantidad:
            raise forms.ValidationError('Debe seleccionar un producto y una cantidad válida.')

        return cleaned_data

DetallePedidoFormSet = modelformset_factory(
    DetallePedido,
    form=DetallePedidoForm,
    extra=1,  
    can_delete=True  # Permitir eliminación de registros
)


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio_unitario', 'cantidad_en_stock']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_en_stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ActualizarStockForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    es_entrada = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="¿Es entrada de stock?"
    )
