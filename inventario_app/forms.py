from django import forms
from django.forms import ModelForm
from inventario_app.models import Product
from django.urls import reverse
from captcha.fields import CaptchaField

class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','description','category','image', 'is_bundle', 'in_stock']
        widgets = {
            'category': forms.CheckboxSelectMultiple(),
        }
        
choices = (
    ('1', 'Gran Rosario'),
    ('2', 'Funes'),
    ('3', 'Roldán')
)

class EmailConfirmationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Nombre')
    surname = forms.CharField(max_length=100, required=True, label='Apellido')
    phone_number = forms.CharField(max_length=20, label='Teléfono')
    location = forms.ChoiceField(choices = choices, label='Localidad')
    customer_address = forms.CharField(max_length=100, label='Dirección')
    email = forms.EmailField(required=False, help_text='Agregue email si desea recibir orden por corre electrónico.')
    gift = forms.BooleanField(label='Para Regalar!', required=False)
    order_items = forms.JSONField(widget=forms.HiddenInput()) 
    captcha = CaptchaField()

    def clean_location(self):
        value = self.cleaned_data.get('location')
        return dict(self.fields['location'].choices)[value]
    