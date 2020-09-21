from django.forms import ModelForm
from inventario_app.models import Product
from django.urls import reverse


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','description','category','image']
       

        
