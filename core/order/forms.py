from django import forms
from .models import Order, OrderItem, Coupon


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'first_name', 'last_name', 'address']


class CouponForm(forms.Form):
    code = forms.CharField(max_length=48)
