from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product
from membership.models import Member
from shopping_cart.models import Cart, CartItem
from .forms import ProductCartForm
import datetime

def product_detail(request, product_pk):
    cart = request.session.get('shopping_cart', -1)
    if int(cart) < 0:
        cart_object = Cart.objects.create(user=request.user)
        cart = cart_object.id
    else :
        cart_object = Cart.objects.get(id=cart)
        
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

            request.session['shopping_cart'] = cart
            return HttpResponse('done : %s : %s' % (total_products, total_prices))


    elif request.method == 'GET':
        form = ProductCartForm()

        product = Product.objects.get(pk=product_pk)
        discount = request.user.member.get_level()['BENEFIT']
        discounted_price = 0
        if not request.user.member.member_type == Member.GUEST and \
            not request.user.member.member_type == Member.NEW_MEMBER:
            discounted_price = product.price * (100 - discount) / 100

        response = render(request, 'storefront/product_detail.html', 
            {'product':product, 'form':form, 'discount': discount, 'discounted_price': int(discounted_price)})

        request.session['shopping_cart'] = cart

    return response

def product_all(request):
    return HttpResponse("OK")

def index(request):
    return HttpResponse("OK")