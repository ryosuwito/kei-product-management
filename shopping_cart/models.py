from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User
import datetime

class Cart(models.Model):
    user = models.ForeignKey(User, related_name="users_cart", on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    last_update = models.DateTimeField(db_index=True,default=datetime.datetime.now)
    is_expired = models.BooleanField(db_index=True,default=False)
    is_checked_out = models.BooleanField(db_index=True,default=False)
    is_paid = models.BooleanField(db_index=True,default=False)
    
    class Meta:
        verbose_name_plural = "Carts"

    def __str__(self):
       return 'Cart%s'%self.pk 
       from .models import CartItem

    def get_total_items_in_cart(self): #cart object
        try :
            if CartItem.objects.filter(cart=self):
                return sum([ i.quantity for i in CartItem.objects.filter(cart=self) ])
        except:
            pass
        return 0                
        

    def get_total_price(self): #cart object
        try :
            if CartItem.objects.filter(cart=self):
                return sum([ i.quantity * i.product.price for i in CartItem.objects.filter(cart=self) ])
        except:
            pass
        return 0




class CartItem(models.Model) :
    quantity = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(Product, related_name="product_in_cart", on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, related_name="item_in_cart", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Cart items"

    def get_item_details(self):
        details = {}
        details['details'] = Product.get_details(self.product)
        details['total_weight'] = self.quantity * self.product.unit_weight
        details['subtotal'] = self.quantity * self.product.price
        return details

    def __str__(self):
       return 'CartItem%s'%self.pk