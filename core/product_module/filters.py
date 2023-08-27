import django_filters
from django import forms
from .models import Product, Brand, ProductSize, ProductColor


class ProductFileter(django_filters.FilterSet):
    price1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=ProductSize.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=ProductColor.objects.all(),
                                                     widget=forms.CheckboxSelectMultiple)
