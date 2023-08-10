from django.urls import path
from .views import all_products,detail_product

app_name = 'product_module'

urlpatterns = [
    path('', all_products, name='products'),
    path('<int:id>', detail_product, name='product-detail'),
    path('cat/<int:id>/', all_products, name='products-by-cat'),
]
