from django.http import HttpResponse
from django.shortcuts import render
from .models import Cart, CartItem
import shopping_cart.carts as carts

def index(request):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    total_products =cart_object.get_total_products()
    total_prices = cart_object.get_total_prices()
    items_in_carts = cart_object.get_items_in_cart()
    product_details = cart_object.get_product_details()

    request.session['shopping_cart'] = cart['cart_id']
    return HttpResponse('done : %s : %s : %s' % (total_products, total_prices, product_details[0]['details']['name']))
