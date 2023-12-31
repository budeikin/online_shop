from django.contrib import admin
from .models import Category, Brand, Product, ProductGallery, Variants, ProductColor, ProductSize, Comment, Chart
import admin_thumbnails


# Register your models here.


class ProductVariantAdminInline(admin.TabularInline):
    model = Variants
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'is_sub']
    prepopulated_fields = {'slug': ('name',)}


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'total_price', 'amount']
    list_filter = ['is_available']
    list_editable = ['amount']
    inlines = [ProductGalleryInline, ProductVariantAdminInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variants)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(Comment)
admin.site.register(ProductGallery)
admin.site.register(Brand)
admin.site.register(Chart)
