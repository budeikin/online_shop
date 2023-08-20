from django.shortcuts import render, redirect
from .models import Order, OrderItem
from .forms import OrderForm
from cart.models import Cart


# Create your views here.
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)

    return render(request, 'order/order.html', context={'order': order})


def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            data = order_form.cleaned_data
            order = Order.objects.create(user_id=request.user.id, email=data['email'], first_name=data['first_name'],
                                         last_name=data['last_name'])
            cart = Cart.objects.filter(user_id=request.user.id)
            for item in cart:
                OrderItem.objects.create(order_id=order.id, user_id=request.user.id, product_id=item.product_id,
                                         variant_id=item.variant_id,
                                         quantity=item.quantity)
            Cart.objects.filter(user_id=request.user.id).delete()
            return redirect('order:order-detail', order.id)
