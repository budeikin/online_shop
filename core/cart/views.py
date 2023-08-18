from django.shortcuts import render,redirect
from product_module.models import Product, Variants
from .models import Cart
from .forms import CartForm


# Create your views here.

def cart_detail(request):
    return render(request, 'cart/cart.html', context={})


def add_to_cart(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    if product.status != 'None':
        var_id = request.POST.get('select')
        data = Cart.objects.filter(user_id=request.user.id, variant_id=var_id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    else:
        data = Cart.objects.filter(user_id=request.user.id, product_id=product_id)
        if data:
            check = 'yes'
        else:
            check = 'no'

    if request.method == 'POST':
        form = CartForm(request.POST)
        var_id = request.POST.get('select')
        if form.is_valid():
            data = form.cleaned_data['quantity']
            if check == 'yes':
                if product.status != "None":
                    shop = Cart.objects.get(user_id=request.user.id, product_id=product_id, variant_id=var_id)

                else:
                    shop = Cart.objects.get(user_id=request.user.id, product_id=product_id)
                shop.quantity += data
                shop.save()

            else:
                Cart.objects.create(user_id=request.user.id, product_id=product_id, quantity=data, variant_id=var_id)
        return redirect(url)
