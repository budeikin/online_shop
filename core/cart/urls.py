from django.urls import path
from .views import cart_detail, add_to_cart,delete_from_cart

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart-detail'),
    path('add/<int:id>/', add_to_cart, name='add-to-cart'),
    path('delete/<int:id>/', delete_from_cart, name='delete-from-cart'),
]
