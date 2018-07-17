from django.http import HttpResponse
from django.shortcuts import render
from .models import Cart, CartItem
import shopping_cart.carts as carts

def index(request):
    cart = carts.get_cart(request)
    return render(request, 'shopping_cart/cart_show_all.html', {'cart':cart['cart_object']})
