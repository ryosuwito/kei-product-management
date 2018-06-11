from django.db import models
from django.contrib.auth.models import User
from shopping_cart.models import Cart
import datetime

class PurchaseOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(db_index=True,default=datetime.datetime.now)
    payment_date = models.DateTimeField(db_index=True,blank=True)
    token_expiry_date = models.DateTimeField(blank=True)
    is_tokenized = models.BooleanField(db_index=True,default=False)
    is_token_expired = models.BooleanField(db_index=True,default=False)
    is_verified = models.BooleanField(db_index=True,default=False)
    is_void = models.BooleanField(db_index=True,default=False)
    payment_status = models.TextField(blank=True)
    payment_token = models.CharField(blank=True)

    class Meta:
        verbose_name = "PurchaseOrder"
        verbose_name_plural = "Purchase Orders"

    def __str__(self):
       return 'Purchase Order No. : %s'%self.pk
