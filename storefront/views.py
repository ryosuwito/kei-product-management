from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from catalog.models import Product, Category
from membership.models import Member
from shopping_cart.models import Cart, CartItem, WishList, WishListItem
from shopping_cart import carts, wishlists
from django.urls import reverse
from membership.views import check_host

import datetime
import random

from .forms import ProductCartForm

def product_detail(request, product_pk):
    referal_code = False
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    all_product = Product.objects.filter(is_archived=False).exclude(pk=product_pk)
    is_wishlist = False
    if len(all_product) >= 5:
        other_product = random.sample(list(all_product), 3)
    else:
        other_product = random.sample(list(all_product), len(all_product))

    product = Product.objects.get(pk=product_pk)
    is_in_wishlist = False

    if request.method == 'POST':
        method = ''
        try:
            method = request.POST['method']
        except:
            pass
        
        if method == 'wishlist':  
            is_wishlist = True 
            wishlist_item = WishListItem.objects.get_or_create(wishlist=wishlist_object, product=product)[0]
       
        elif method == 'cart':
            form = ProductCartForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                quantity = data.get('quantity')
                cart_item = False
                try :
                    cart_item = CartItem.objects.get_or_create(cart=cart_object, product=product)[0]
                except:
                    pass

                if not cart_item.quantity :
                    cart_item.quantity = quantity
                else :
                    cart_item.quantity += int(quantity)
                cart_item.save()
            
            return HttpResponseRedirect(reverse('cart:index', 
                current_app=request.resolver_match.namespace))

    form = ProductCartForm()

    product = Product.objects.get(pk=product_pk)

    discount = 0
    discounted_price = product.price
    
    if request.user.is_authenticated:
        if not request.user.member.member_type == Member.GUEST and \
            not request.user.member.member_type == Member.NEW_MEMBER:
            discount = request.user.member.get_level()['BENEFIT']
            discounted_price = product.price * (100 - discount) / 100

    products_in_wishlist = [x.product.id for x in wishlist_object.item_in_wishlist.all()]
    for pk in products_in_wishlist:
        if product_pk == pk:
            is_in_wishlist = True

    if is_wishlist:
        response = HttpResponseRedirect(reverse("storefront:product_detail", kwargs=
            {'product_pk':product_pk})[:-1]+"#formQuantity")
    else:
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
    try:
        product_list = Product.objects.filter(is_archived=False)
    except:
        product_list=''
    if not product_list:
        product_title = 'Tidak Ada Produk'
    else:
        product_title = 'Menampilkan Semua Produk'
    return paginate_results(request, product_list,product_title)
    
def product_by_category(request, category_pk):
    try:
        kategori = Category.objects.get(pk=category_pk)
        product_list = kategori.products_in_category.filter(is_archived=False)
    except:
        product_list=''
    if not product_list:
        product_title = 'Tidak Ada Produk'
    else:
        product_title = 'Menampilkan Semua Produk %s' % (kategori.name.title())
    return paginate_results(request, product_list,product_title)

def paginate_results(request, product_list,product_title):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    max_page = 4
    min_page = 0
    products = ''
    if product_list:
        try:
            paginator = Paginator(product_list,12)
            page = request.GET.get('page', 1)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            max_page = products.number + 4
            min_page = products.number - 4
        except:
            pass

    try:
        categories = Category.objects.filter(is_archived=False)
    except:
        categories = ''

    response = render(request, 'storefront/product_all.html', 
        {'cart':cart_object,
         'wishlist':wishlist_object, 
         'products':products,
         'categories':categories,
         'product_title':product_title,
         'max_page':max_page,
         'min_page':min_page})
    return response