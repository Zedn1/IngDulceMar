from django import forms
from django.forms import modelformset_factory
from .models import Pedido, DetallePedido

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
