from django.urls import path
from .views import all_products, detail_product, product_like, product_unlike,product_comment

app_name = 'product_module'

urlpatterns = [
    path('', all_products, name='products'),
    path('<int:id>/', detail_product, name='product-detail'),
    path('cat/<slug>/', all_products, name='products-by-cat'),
    path('like/<int:id>/', product_like, name='product-like'),
    path('unlike/<int:id>/', product_unlike, name='product-unlike'),
    path('comment/<int:id>/', product_comment, name='product-comment'),
]
