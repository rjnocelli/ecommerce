from django import forms
from django.forms import ModelForm
from inventario_app.models import Product
from django.urls import reverse


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','description','category','image']

class EmailConfirmationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Nombre')
    surname = forms.CharField(max_length=100, required=True, label='Apellido')
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, label='Telefono')


       

        
