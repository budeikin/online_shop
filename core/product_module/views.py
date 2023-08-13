from django.shortcuts import render
from .models import Product, Category, Variants
from django.shortcuts import get_object_or_404


# Create your views here.

def all_products(request, slug=None):
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub=False)
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)

    return render(request, 'product_module/products.html',
                  context={'products': products, 'categories': categories})


def detail_product(request, id):
    product = get_object_or_404(Product, id=id)
    similar = product.tags.similar_objects()[:2]
    if product.status != 'None':
        if request.method == 'POST':
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('selected_variant')
            variants = Variants.objects.get(id=var_id)
        else:
            variant = Variants.objects.filter(product_variant_id=id)
            variants = Variants.objects.get(id=variant.first().id)
        context = {
            'product': product, 'variant': variant, 'variants': variants, 'similar_products': similar
        }
        return render(request, 'product_module/product_detail.html', context)

    return render(request, 'product_module/product_detail.html',
                  context={'product': product, 'similar_products': similar})
