from django.shortcuts import render
from django.http.response import HttpResponse


# Create your views here.

def cart_detail(request):
    return render(request, 'cart/cart.html', context={})
