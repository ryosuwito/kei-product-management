from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User
import datetime

class Cart(models.Model):
    user = models.ForeignKey(User, related_name="users_cart", on_delete=models.SET_NULL)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    last_update = models.DateTimeField(default=datetime.datetime.now)
    is_expired = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Carts"

    def __str__(self):
       return 'Cart%s'%self.pk


class CartItem(models.Model) :
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, related_name="product_in_cart", on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart, related_name="item_in_cart", on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Carts"

    def get_item_details(self):
        details = Product.get_details(self.product)
        return details

    def __str__(self):
       return 'Cart%s'%self.pk