from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, Coupon
from .forms import OrderForm, CouponForm
from cart.models import Cart
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.utils.crypto import get_random_string


# Create your views here.
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user_id=request.user.id)
    form = CouponForm()
    return render(request, 'order/order.html', context={'order': order, 'form': form})


def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            data = order_form.cleaned_data
            code = get_random_string(length=8)
            order = Order.objects.create(user_id=request.user.id, email=data['email'],
                                         first_name=data['first_name'],
                                         last_name=data['last_name'],
                                         code=code)
            cart = Cart.objects.filter(user_id=request.user.id)
            for item in cart:
                OrderItem.objects.create(order_id=order.id, user_id=request.user.id, product_id=item.product_id,
                                         variant_id=item.variant_id,
                                         quantity=item.quantity)
            Cart.objects.filter(user_id=request.user.id).delete()
            return redirect('order:order-detail', order.id)


@require_POST
def order_coupon(request, order_id):
    url = request.META.get('HTTP_REFERER')
    form = CouponForm(request.POST)
    time = timezone.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(name__exact=code, start__lte=time, end__gte=time, is_active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'this code does not exist', 'danger')
            return redirect('order:order-detail', order_id)

        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
        return redirect(url)
