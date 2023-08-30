from django import forms
from .models import Cart, Compair


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']


class CompairForm(forms.ModelForm):
    class Meta:
        model = Compair
        fields = ['product']
