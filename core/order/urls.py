from django.urls import path
from .views import order_detail

app_name = 'order'

urlpatterns = [
    path('',order_detail,name='order-detail')
]
