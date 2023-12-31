from django.urls import path
from .views import cart_detail, add_to_cart, delete_from_cart, add_single, remove_single, compare, show

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart-detail'),
    path('add/<int:id>/', add_to_cart, name='add-to-cart'),
    path('delete/<int:id>/', delete_from_cart, name='delete-from-cart'),
    path('add_single/<int:id>/', add_single, name='add-single'),
    path('remove_single/<int:id>/', remove_single, name='remove-single'),
    path('compare/<int:id>/', compare, name='product-compare'),
    path('show/', show, name='show-compare'),

]
