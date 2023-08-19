from django.shortcuts import render, redirect
from product_module.models import Product, Variants
from .models import Cart
from .forms import CartForm


# Create your views here.

def cart_detail(request):
    items = Cart.objects.filter(user_id=request.user.id)
    total = 0
    for item in items:
        if item.product.status != 'None':
            total += item.variant.total_price * item.quantity
        else:
            total += item.product.total_price * item.quantity
    return render(request, 'cart/cart.html', context={'items': items, 'total': total})


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


def delete_from_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Cart.objects.filter(product_id=id)
    product.delete()
    return redirect(url)
