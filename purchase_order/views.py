from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from shopping_cart.models import Cart, CartItem, WishListItem
import shopping_cart.carts as carts
import shopping_cart.wishlists as wishlists
from membership.models import Member
from shipping_backend.shipping_check import get_courier, get_cost
from django.middleware.csrf import get_token

@login_required
def index(request):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    shipping_cost = cart_object.shipping_cost
    services = ''
    selected_service = ''
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    products = cart_object.get_items_in_cart();
    discount = 0
    discounted_price = 0

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
                request.session['services'] = services
                
            return JsonResponse(list(services), safe=False)

        elif method == 'set_shipping':
            if 'services' in request.session :
                services= request.session['services']
            user_selected_service = request.POST.get('service')
            for s in services:
                if s['service'] == user_selected_service :
                    cart_object.shipping_cost = s['cost'][0]['int_value']
                    cart_object.save()
                    break

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
        'selected_service':selected_service,
        'token':token,})

def checkout(request):
    pass

def history(request):
    pass