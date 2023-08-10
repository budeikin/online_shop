from django.shortcuts import render
from .models import Product, Category
from django.shortcuts import get_object_or_404


# Create your views here.

def all_products(request, slug=None):
    products = Product.objects.all()
    category = Category.objects.all()
    if slug:
        category = Category.objects.get(slug=slug)
        products = Product.objects.filter(category=category)

    return render(request, 'product_module/products.html', context={'products': products, 'category': category})


def detail_product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_module/product_detail.html', context={'product': product})
