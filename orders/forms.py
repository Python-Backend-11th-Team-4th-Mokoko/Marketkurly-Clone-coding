from django import forms

from shop.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'product_name', 'slug', 'image', 'description',
            'stock', 'price', 'available', 'delivery', 'packaging', 'seller',
        ]
