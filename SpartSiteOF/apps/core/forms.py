from allauth.account.forms import SignupForm
from django import forms
from .models import *


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="Nombre")
    last_name = forms.CharField(max_length=30, label="Apellido")

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = ["sku", "nombre", "descripcion", "imagen", "periodo"]
