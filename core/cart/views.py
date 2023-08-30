from django.shortcuts import render, redirect, get_object_or_404
from product_module.models import Product, Variants
from .models import Cart, Compair
from .forms import CartForm, CompairForm
from django.contrib.auth.decorators import login_required
from order.forms import OrderForm
from django.contrib import messages


# Create your views here.
@login_required(login_url='accounts:login')
def cart_detail(request):
    items = Cart.objects.filter(user_id=request.user.id)
    user = request.user
    order_form = OrderForm()
    total = 0
    for item in items:
        if item.product.status != 'None':
            total += item.variant.total_price * item.quantity
        else:
            total += item.product.total_price * item.quantity
    return render(request, 'cart/cart.html',
                  context={'items': items, 'total': total, 'order_form': order_form, 'user': user})


@login_required(login_url='accounts:login')
def add_to_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    if product.status != 'None':
        var_id = request.POST.get('select')
        data = Cart.objects.filter(user_id=request.user.id, variant_id=var_id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    else:
        data = Cart.objects.filter(user_id=request.user.id, product_id=id)
        if data:
            check = 'yes'
        else:
            check = 'no'

    if request.method == 'POST':
        form = CartForm(request.POST)
        var_id = request.POST.get('select')
        if form.is_valid():
            info = form.cleaned_data['quantity']
            if check == 'yes':
                if product.status != "None":
                    shop = Cart.objects.get(user_id=request.user.id, product_id=id, variant_id=var_id)
                else:
                    shop = Cart.objects.get(user_id=request.user.id, product_id=id)
                shop.quantity += info
                shop.save()
            else:
                Cart.objects.create(user_id=request.user.id, product_id=id, quantity=info, variant_id=var_id)
        else:
            form.add_error('quantity', 'something is wrong')

    return redirect(url)


@login_required(login_url='accounts:login')
def delete_from_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Cart.objects.filter(product_id=id)
    product.delete()
    return redirect(url)


def add_single(request, id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    if cart.product.status == 'None':
        product = Product.objects.get(id=cart.product.id)
        if product.amount > cart.quantity:
            cart.quantity += 1
    else:
        variant = Variants.objects.get(id=cart.variant.id)
        if variant.amount > cart.quantity:
            cart.quantity += 1
    cart.save()
    return redirect(url)


def remove_single(request, id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    if cart.quantity < 2:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()
    return redirect(url)


def compare(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        item = get_object_or_404(Product, id=id)
        qs = Compair.objects.filter(user_id=request.user.id, product_id=id)
        if qs.exists():
            messages.success(request, 'ook')
        else:
            Compair.objects.create(user_id=request.user.id, product_id=item.id, session_key=None)
    else:
        item = get_object_or_404(Product, id=id)
        qs = Compair.objects.filter(user_id=None, product_id=id, session_key=request.session.session_key)
        if qs.exists():
            messages.success(request, 'ok session')
        else:
            if not request.session.session_key:
                request.session.create()
            Compair.objects.create(user_id=None, product_id=item.id, session_key=request.session.session_key)
    return redirect(url)


def show(request):
    if request.user.is_authenticated:
        data = Compair.objects.filter(user_id=request.user.id)
        return render(request, 'cart/show.html', {'data': data})
    else:
        data = Compair.objects.filter(session_key__exact=request.session.session_key, user_id=None)
        return render(request, 'cart/show.html', {'data': data})
