from django.http import HttpResponse
from django.shortcuts import render
from .models import Cart, CartItem, WishListItem
import shopping_cart.carts as carts
import shopping_cart.wishlists as wishlists

def index(request):
    cart = carts.get_cart(request)
    wishlist = wishlists.get_wishlist(request)
    if request.method == 'POST':
        item=""
        try :
            if request.POST['item'] :
                item_pk = request.POST['item'].split('_')[1]
                item = CartItem.objects.get(pk=item_pk)
                item.delete()
        except:
            pass
    return render(request, 'shopping_cart/cart_show_all.html', {'wishlist': wishlist['wishlist_object'],'cart':cart['cart_object']})

def wishlist_index(request):
    cart = carts.get_cart(request)
    wishlist = wishlists.get_wishlist(request)
    if request.method == 'POST':
        item=""
        try :
            if request.POST['item'] :
                item_pk = request.POST['item'].split('_')[1]
                item = WishListItem.objects.get(pk=item_pk)
                item.delete()
        except:
            pass
    return render(request, 'shopping_cart/wishlist_show_all.html', {'cart':cart['cart_object'], 'wishlist': wishlist['wishlist_object']})