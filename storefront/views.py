from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product
from membership.models import Member
from shopping_cart.models import Cart, CartItem
from .forms import ProductCartForm
from shopping_cart import carts
import datetime

def product_detail(request, product_pk):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
        
        
    if request.method == 'POST':
        form = ProductCartForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            quantity = data.get('quantity')
            product = Product.objects.get(pk=product_pk)

            cart_item = False
            try :
                cart_item = CartItem.objects.get(cart=cart_object, product=product)
            except:
                pass

            if not cart_item :
                cart_item = CartItem.objects.create(cart=cart_object, product=product)

            if not cart_item.quantity :
                cart_item.quantity = quantity
            else :
                cart_item.quantity += int(quantity)
            cart_item.save()

            cart_object.last_update = datetime.datetime.now()
            cart_object.save()
            total_products = cart_object.get_total_items_in_cart()
            total_prices = cart_object.get_total_price()

    form = ProductCartForm()

    product = Product.objects.get(pk=product_pk)
    discount = request.user.member.get_level()['BENEFIT']
    discounted_price = 0
    if not request.user.member.member_type == Member.GUEST and \
        not request.user.member.member_type == Member.NEW_MEMBER:
        discounted_price = product.price * (100 - discount) / 100

    response = render(request, 'storefront/product_detail.html', 
        {'product':product, 'cart':cart_object, 'form':form, 'discount': discount, 'discounted_price': int(discounted_price)})

    request.session['shopping_cart'] = cart['cart_id']

    return response

def index(request):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    product = Product.objects.all();
    response = render(request, 'storefront/product_all.html', {'cart':cart_object,'products':product})
    return response