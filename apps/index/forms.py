from django import forms
from django.forms import ModelForm

from index.models import Product


class ProductForm(forms.Form, ModelForm):
    class Meta:
        model = Product
        fields = ['product_title', 'product_price', 'number', 'brush_price', 'key_word']
