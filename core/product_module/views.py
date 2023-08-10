from django.shortcuts import render
from .models import Product, Category


# Create your views here.

def all_products(request, id=None):
    products = Product.objects.all()
    category = Category.objects.all()
    if id:
        category = Category.objects.get(id=id)
        products = Product.objects.filter(category=category)

    return render(request, 'product_module/products.html', context={'products': products, 'category': category})


def detail_product(request,id):
    product = Product.objects.get(id=id)
    return render(request,'product_module/product_detail.html',context={'product':product})