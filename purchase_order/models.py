from django.db import models
from django.contrib.auth.models import User
from shopping_cart.models import Cart
import datetime

class PurchaseOrder(models.Model):
    user = models.ForeignKey(User, related_name="users_order", on_delete=models.SET_NULL, null=True)
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(db_index=True,default=datetime.datetime.now)
    payment_date = models.DateTimeField(null=True, db_index=True, blank=True)
    token_expiry_date = models.DateTimeField(null=True, blank=True)
    is_tokenized = models.BooleanField(db_index=True,default=False)
    is_token_expired = models.BooleanField(db_index=True,default=False)
    is_verified = models.BooleanField(db_index=True,default=False)
    is_void = models.BooleanField(db_index=True,default=False)
    payment_status = models.TextField(blank=True)
    payment_token = models.CharField(null=True, max_length=50, blank=True)

    class Meta:
        verbose_name = "PurchaseOrder"
        verbose_name_plural = "Purchase Orders"

    def __str__(self):
       return 'Purchase Order No. : %s'%self.pk

