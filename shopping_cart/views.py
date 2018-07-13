from django.http import HttpResponse
from django.shortcuts import render
from .models import Cart, CartItem

def index(request):
    cart = request.session.get('shopping_cart', -1)
    if int(cart) < 0:
        cart_object = Cart.objects.create(user=request.user)
        cart = cart_object.id
    else :
        cart_object = Cart.objects.get(id=cart)
    
    total_products = cart_object.get_total_items_in_cart()
    total_prices = cart_object.get_total_price()
    items_in_carts = CartItem.objects.filter(cart=cart_object)
    product_details = [x.get_item_details()  for x in items_in_carts]

    request.session['shopping_cart'] = cart
    return HttpResponse('done : %s : %s : %s' % (total_products, total_prices, product_details[0]['details']['name']))
