from django.shortcuts import render
from django.http.response import HttpResponse
from product_module.models import Category, Product
from .forms import SearchForm
from django.db.models import Q


# Create your views here.

def home_page(request):
    categories = Category.objects.filter(is_sub=False)
    form = SearchForm()
    return render(request, 'home_module/home_page.html', context={'categories': categories, 'form': form})


def search_page(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data.get('search')
            if search_text is not None:
                products = Product.objects.filter(
                    Q(name__icontains=search_text) | Q(description__icontains=search_text))
            return render(request, 'product_module/products.html', context={'products': products, 'form': form})
