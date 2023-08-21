from django.urls import path
from .views import order_detail, order_create,order_coupon

app_name = 'order'

urlpatterns = [
    path('<int:order_id>/', order_detail, name='order-detail'),
    path('create/', order_create, name='order-create'),
    path('coupon/<int:order_id>/', order_coupon, name='order-coupon'),
]
