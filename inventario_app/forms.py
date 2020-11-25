from django import forms
from django.forms import ModelForm
from inventario_app.models import Product
from django.urls import reverse
from captcha.fields import CaptchaField
from phonenumber_field.formfields import PhoneNumberField

class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','description','category','image', 'is_bundle', 'in_stock']
        widgets = {
            'category': forms.CheckboxSelectMultiple(),
        }
        

class EmailConfirmationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Nombre')
    surname = forms.CharField(max_length=100, required=True, label='Apellido')
    phone_number = forms.CharField(max_length=20, label='Telefono')
    # phone = PhoneNumberField(label='Telefono')
    email = forms.EmailField(required=False, help_text='Agregue email si desea recibir orden por corre electrónico.')
    gift = forms.BooleanField(label='Para Regalar!', required=False)
    order_items = forms.JSONField(widget=forms.HiddenInput()) 
    captcha = CaptchaField()
    