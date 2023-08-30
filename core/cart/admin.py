from django.contrib import admin
from .models import Cart, Compair


# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'variant', 'product', 'quantity']


admin.site.register(Cart, CartAdmin)
admin.site.register(Compair)
