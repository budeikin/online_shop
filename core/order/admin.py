from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['user', 'product', 'variant', 'size','color', 'quantity']
    extra = 2


class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_paid']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
