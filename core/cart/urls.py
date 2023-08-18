from django.urls import path
from .views import cart_detail,add_to_cart

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart-detail'),
    path('add/<int:product_id>/', add_to_cart, name='add-to-cart')
]
