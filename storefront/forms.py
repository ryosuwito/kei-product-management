from django import forms
from shopping_cart.models import Cart, CartItem

class ProductCartForm (forms.Form):
    quantity = forms.IntegerField(required=True, initial=1)
