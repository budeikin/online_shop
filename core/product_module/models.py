from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub', blank=True, null=True)
    is_sub = models.BooleanField(default=False)
    slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='category', blank=True, null=True)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('product_module:products-by-cat', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    VARIANT = (
        ('None', 'none'),
        ('Size', 'size'),
        ('Color', 'color'),
    )

    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True)
    total_price = models.PositiveIntegerField()
    description = RichTextUploadingField(null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    tags = TaggableManager(blank=True)
    status = models.CharField(max_length=255, null=True, blank=True, choices=VARIANT)
    image = models.ImageField(upload_to='products')
    like = models.ManyToManyField(User, blank=True, related_name='product_like')
    unlike = models.ManyToManyField(User, blank=True, related_name='product_unlike')
    total_like = models.PositiveIntegerField(default=0)
    total_unlike = models.PositiveIntegerField(default=0)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('product_module:product-detail', kwargs={'id': self.id})

    def __str__(self):
        return f"{self.name}"

    def total_like(self):
        return self.like.count()

    def total_unlike(self):
        return self.unlike.count()

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


class ProductGallery(models.Model):
    image = models.ImageField(upload_to='gallery')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product


class ProductSize(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductColor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Variants(models.Model):
    name = models.CharField(max_length=255)
    product_variant = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variant')
    size_variant = models.ForeignKey(ProductSize, on_delete=models.CASCADE, blank=True, null=True)
    color_variant = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True)
    total_price = models.PositiveIntegerField()

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price
