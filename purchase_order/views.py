from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from shopping_cart.models import Cart, CartItem, WishListItem
import shopping_cart.carts as carts
import shopping_cart.wishlists as wishlists
from membership.models import Member
from shipping_backend.shipping_check import get_courier, get_cost
from django.middleware.csrf import get_token
from shipping_backend.models import ShippingOrigin
from django.forms.models import model_to_dict
from .models import PurchaseOrder, PurchaseOrderItem
from membership.templatetags.int_to_rupiah import int_to_rupiah
from django.urls import reverse
import datetime

@login_required
def index(request):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    services = ''
    selected_service = ''
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']

    if not cart_object.get_total_items_in_cart():
        return HttpResponseRedirect(reverse('cart:index'))
        
    products = cart_object.get_items_in_cart()
    discount = 0
    discounted_price = 0
    shipping_origin = ShippingOrigin.objects.filter(is_default = True)[0]
    if 'old_cart_weight' in request.session:
        if request.session['old_cart_weight'] != cart_object.get_total_weight():
            cart_object.shipping_cost = 0
            cart_object.save()
            request.session['old_cart_weight'] = cart_object.get_total_weight()
    else:
        request.session['old_cart_weight'] = cart_object.get_total_weight()

    if request.method == 'POST':
        method = request.POST.get('method', 'remove')
        item=""
        if method == 'check_shipping':
            costs_list = ''
            costs_list = get_cost(request.user, request.POST.get('courier', 'jne').lower())
            if costs_list:
                services = [x for x in costs_list]
                selected_service = request.POST['courier']
                cart_object.shipping_service = selected_service
                cart_object.save()
                request.session['services'] = services
                
            return JsonResponse(list(services), safe=False)

        elif method == 'set_shipping':
            if 'services' in request.session :
                services= request.session['services']
            user_selected_service = request.POST.get('service')
            for s in services:
                if s['service'] == user_selected_service :
                    cart_object.shipping_sub_service = user_selected_service
                    cart_object.shipping_cost = s['cost'][0]['int_value']
                    cart_object.save()
                    break
                    
    if cart_object.shipping_cost != 0 and cart_object.get_total_items_in_cart() == 0:
        shipping_cost = 0
    else:
        shipping_cost = cart_object.shipping_cost
        
    if request.user.is_authenticated:
        discounted_price = cart_object.get_total_price()
        if not request.user.member.member_type == Member.GUEST and \
            not request.user.member.member_type == Member.NEW_MEMBER:
            benefit = request.user.member.get_level()['BENEFIT']
            discount = cart_object.get_total_price() * discount / 100
            discounted_price = cart_object.get_total_price() * (100 - discount) / 100
    if shipping_cost:
        discounted_price += shipping_cost

    couriers = get_courier()
    token = get_token(request)
    return render(request, 'purchase_order/select_shipping.html', 
        {'wishlist': wishlist_object,
        'cart':cart_object,
        'products':products,
        'discount':discount,
        'discounted_price':discounted_price,
        'couriers':couriers,
        'shipping_cost':shipping_cost,
        'services':services,
        'shipping_origin':shipping_origin,
        'selected_service':selected_service,
        'token':token,})

@login_required
def checkout(request):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    if not cart_object.get_total_items_in_cart():
        return HttpResponseRedirect(reverse('cart:index'))
    products = cart_object.get_items_in_cart()

    discount = 0
    discounted_price = 0

    if request.user.is_authenticated:
        discounted_price = cart_object.get_total_price()
        if not request.user.member.member_type == Member.GUEST and \
            not request.user.member.member_type == Member.NEW_MEMBER:
            benefit = request.user.member.get_level()['BENEFIT']
            discount = cart_object.get_total_price() * discount / 100
            discounted_price = cart_object.get_total_price() * (100 - discount) / 100


    order = PurchaseOrder.objects.get_or_create(user=request.user, is_paid=False, is_checked_out=False)[0]
    for item in products:
        order_item = PurchaseOrderItem.objects.create(purchase_order = order)
        order_item.quantity = item.quantity
        order_item.product = item.product
        order_item.save()

    order.total_price = discounted_price
    order.discount = discount
    order.shipping_cost = cart_object.shipping_cost
    order.total_payment = discounted_price + cart_object.shipping_cost
    order.alamat_tujuan = request.user.member.get_home_address()
    order.service = cart_object.shipping_service.upper()
    order.sub_service = cart_object.shipping_sub_service
    order.save()
    order_detail = {key: format_order(key, value) for (key, value) in model_to_dict(order, 
            fields=["order_number",
                    "total_price", 
                    "total_payment", 
                    "shipping_cost", 
                    "alamat_tujuan",
                    "service",
                    "sub_service",
                    "discount"]).items()}
    return JsonResponse(order_detail, safe=False)

@login_required
def pay(request):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    if not cart_object.get_total_items_in_cart():
        return HttpResponseRedirect(reverse('cart:index'))
    cart_object.delete()
    order = PurchaseOrder.objects.filter(user=request.user, is_paid=False, is_checked_out = False)[0]
    order.is_checked_out = True
    order.is_paid = True
    order.is_verified = True
    order.payment_date = datetime.datetime.now()
    order.save()
    del request.session['shopping_cart']
    cart = carts.get_cart(request)
    return JsonResponse(model_to_dict(order), safe=False)


@login_required
def history(request):
    pass

def format_order(key, value):
    for x in ["order_number", "alamat_tujuan", "service", "sub_service"]:
        if key == x :
            return value
    return(int_to_rupiah(value))