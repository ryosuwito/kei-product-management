from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product
from membership.models import Member
from shopping_cart.models import Cart, CartItem, WishList, WishListItem
from .forms import ProductCartForm
from shopping_cart import carts, wishlists
import datetime
import random

def product_detail(request, product_pk):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    other_product = random.sample(list(Product.objects.all()), 5)       
    product = Product.objects.get(pk=product_pk)
    is_in_wishlist = False

    if request.method == 'POST':
        method = ''
        try:
            method = request.POST['method']
        except:
            pass
        
        if method == 'wishlist':   
            wishlist_item = WishListItem.objects.get_or_create(wishlist=wishlist_object, product=product)

        elif method == 'cart':
            form = ProductCartForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                quantity = data.get('quantity')
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

    form = ProductCartForm()

    product = Product.objects.get(pk=product_pk)
    if request.user.is_authenticated:
        discount = request.user.member.get_level()['BENEFIT']
        discounted_price = 0
        if not request.user.member.member_type == Member.GUEST and \
            not request.user.member.member_type == Member.NEW_MEMBER:
            discounted_price = product.price * (100 - discount) / 100
    else:
        discount = 0
        discounted_price = 0

    products_in_wishlist = [x.product.id for x in wishlist_object.item_in_wishlist.all()]
    for pk in products_in_wishlist:
        if product_pk == pk:
            is_in_wishlist = True

    response = render(request, 'storefront/product_detail.html', 
        {'product':product, 
        'other_product':other_product, 
        'cart':cart_object, 
        'wishlist':wishlist_object, 
        'form':form, 
        'is_in_wishlist': is_in_wishlist,
        'discount': discount, 
        'discounted_price': int(discounted_price)})

    return response

def index(request):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    product_list = Product.objects.all();
    paginator = Paginator(product_list,7)

    page = request.GET.get('page', 1)
    max_page = 4
    min_page = 0
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    max_page = products.number + 4
    min_page = products.number - 4

    response = render(request, 'storefront/product_all.html', 
        {'cart':cart_object,
         'wishlist':wishlist_object, 
         'products':products,
         'max_page':max_page,
         'min_page':min_page})
    return response