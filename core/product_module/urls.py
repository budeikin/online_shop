from django.urls import path
from .views import all_products

app_name = 'product_module'

urlpatterns = [
    path('', all_products, name='products')
]
