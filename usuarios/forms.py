from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Perfil

class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Contraseña',
        help_text="Debe tener al menos 8 caracteres, incluir números, mayúsculas, minúsculas y símbolos.",
    )
    password_confirmacion = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirmar Contraseña',
    )
    rol = forms.ChoiceField(choices=Perfil.ROLES, label='Rol')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmacion', 'rol']

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['password_confirmacion'].widget.attrs.update({'class': 'form-control'})
        self.fields['rol'].widget.attrs.update({'class': 'form-control'})

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)  # Llama a los validadores configurados en settings.py
        return password

    def clean_password_confirmacion(self):
        password = self.cleaned_data.get('password')
        password_confirmacion = self.cleaned_data.get('password_confirmacion')
        if password and password_confirmacion and password != password_confirmacion:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password_confirmacion