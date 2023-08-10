from django.shortcuts import render
from django.http.response import HttpResponse
from product_module.models import Category


# Create your views here.

def home_page(request):
    categories = Category.objects.all()
    return render(request, 'home_module/home_page.html', context={'categories': categories})


