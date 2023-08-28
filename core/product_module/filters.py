import django_filters
from django import forms
from .models import Product, Brand, ProductSize, ProductColor

price_choice = {
    ('cheapest', 'Cheapest',),
    ('expensive', 'MostExpensive')
}

created_date = {
    ('newest', 'Newest',),
    ('oldest', 'Oldest',),
}

discount = {
    ('higher', 'higher_discount'),
    ('lower', 'lower_discount'),
}


class ProductFileter(django_filters.FilterSet):
    price1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=ProductSize.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=ProductColor.objects.all(),
                                                     widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=price_choice, method='price_filter')
    created_at = django_filters.ChoiceFilter(choices=created_date, method='create_date_filter')
    discount = django_filters.ChoiceFilter(choices=discount, method='discount_filter')

    def price_filter(self, queryset, name, value):
        data = 'unit_price' if value == 'cheapest' else '-unit_price'
        return queryset.order_by(data)

    def create_date_filter(self, queryset, name, value):
        data = 'created_at' if value == 'oldest' else '-created_at'
        return queryset.order_by(data)

    def discount_filter(self, queryset, name, value):
        data = '-discount' if value == 'higher' else 'discount'
        return queryset.order_by(data)
