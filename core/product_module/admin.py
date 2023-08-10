from django.contrib import admin
from .models import Category, Product, ProductGallery


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'total_price']
    list_filter = ['is_available']
    inlines = [ProductGalleryInline, ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
