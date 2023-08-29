from django.db import models
from django.contrib.auth.models import User
from product_module.models import Product, Variants


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    code = models.CharField(max_length=255, null=True)

    def get_price(self):
        total = sum(i.price() for i in self.items.all())
        if self.discount:
            price = (self.discount / 100) * total
            return int(total - price)
        return total

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.username

    def size(self):
        return self.variant.size_variant.name

    def color(self):
        return self.variant.color_variant.name

    def price(self):
        if self.product.status != "None":
            return self.variant.total_price * self.quantity
        else:
            return self.product.total_price * self.quantity


class Coupon(models.Model):
    name = models.CharField(max_length=48, unique=True)
    is_active = models.BooleanField(default=False)
    discount = models.PositiveIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name
