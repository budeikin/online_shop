from django.shortcuts import render, redirect
from .models import Product, Category, Variants, Comment, ProductGallery
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import CommentForm, ReplyCommentForm
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from cart.forms import CartForm
from django.core.paginator import Paginator


# Create your views here.

def all_products(request, slug=None):
    products = Product.objects.all()
    paginator = Paginator(products, 2)
    page_num = request.GET.get('page')
    page_object = paginator.get_page(page_num)
    categories = Category.objects.filter(is_sub=False)
    if slug:
        category = get_object_or_404(Category, slug=slug)
        page_object = Product.objects.filter(category=category)
        paginator = Paginator(page_object, 2)
        page_num = request.GET.get('page')
        page_object = paginator.get_page(page_num)

    return render(request, 'product_module/products.html',
                  context={'products': page_object, 'categories': categories, 'page_num': page_num})


def detail_product(request, id):
    product = get_object_or_404(Product, id=id)
    images = ProductGallery.objects.filter(product_id=id)
    similar = product.tags.similar_objects()[:2]
    comment_form = CommentForm()
    reply_form = ReplyCommentForm()
    cart_form = CartForm()
    comments = Comment.objects.filter(product_id=id, is_reply=False)
    is_like = False
    is_favorite = False

    if product.like.filter(id=request.user.id).exists():
        is_like = True

    if product.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        is_unlike = True

    if product.status != 'None':
        if request.method == 'POST':
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('selected_variant')
            variants = Variants.objects.get(id=var_id)
        else:
            variant = Variants.objects.filter(product_variant_id=id)
            variants = Variants.objects.get(id=variant[0].id)
        context = {
            'product': product, 'variant': variant, 'variants': variants, 'similar_products': similar,
            'is_like': is_like, 'is_unlike': is_unlike, 'form': comment_form, 'comments': comments, 'images': images,
            'reply_form': reply_form, 'cart_form': cart_form, 'is_favorite': is_favorite
        }
        return render(request, 'product_module/product_detail.html', context)

    return render(request, 'product_module/product_detail.html',
                  context={'product': product, 'similar_products': similar, 'is_like': is_like, 'is_unlike': is_unlike
                      , 'form': comment_form, 'comments': comments, 'reply_form': reply_form, 'images': images,
                           'cart_form': cart_form, 'is_favorite': is_favorite})


def product_like(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        is_like = False
    else:
        product.like.add(request.user)
        is_like = True
        messages.success(request, 'thanks for like', 'success')
    return redirect(url)


def product_unlike(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_like = False
    if product.unlike.filter(id=request.user.id).exists():
        product.unlike.remove(request.user)
        is_like = False
    else:
        product.unlike.add(request.user)
        is_like = True
        messages.success(request, 'successfully', 'success')
    return redirect(url)


@login_required(login_url='accounts:login')
def product_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Comment.objects.create(body=data['body'], rate=data['rate'], user_id=request.user.id, product_id=id)
        return redirect(url)


@login_required(login_url='accounts:login')
def comment_reply(request, product_id, comment_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        reply_form = ReplyCommentForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comment.objects.create(body=data['body'], product_id=product_id, user_id=request.user.id,
                                   reply_id=comment_id,
                                   is_reply=True)
            messages.success(request, 'successfully', 'primary')
            return redirect(url)

        return redirect(url)


@login_required(login_url='accounts:login')
def comment_like(request, comment_id):
    url = request.META.get('HTTP_REFERER')
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.comment_like.filter(id=request.user.id).exists():
        comment.comment_like.remove(request.user)
    else:
        comment.comment_like.add(request.user)

    return redirect(url)


def favorite_product(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    is_favorite = False
    if product.favorite.filter(id=request.user.id).exists():
        product.favorite.remove(request.user)
        is_favorite = False
    else:
        product.favorite.add(request.user)
        is_favorite = True
        product.save()
    return redirect(url)
