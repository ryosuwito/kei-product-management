from django.http import HttpResponse
from django.shortcuts import render
from .models import Cart, CartItem
import shopping_cart.carts as carts

def index(request):
    cart = carts.get_cart(request)
    if request.method == 'POST':
        item=""
        try :
            if request.POST['item'] :
                item_pk = request.POST['item'].split('_')[1]
                item = CartItem.objects.get(pk=item_pk)
                item.delete()
        except:
            pass
    return render(request, 'shopping_cart/cart_show_all.html', {'cart':cart['cart_object']})
