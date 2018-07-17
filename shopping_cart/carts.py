from .models import Cart, CartItem

def get_cart(request):
    cart_id = request.session.get('shopping_cart', -1)
    if int(cart_id) < 0:
        cart_object = Cart.objects.create(user=request.user)
        cart_id = cart_object.id
    else :
        cart_object = Cart.objects.get(id=cart_id)    
    request.session['shopping_cart'] = cart_id
    return {'cart_object':cart_object,'cart_id':cart_id}
