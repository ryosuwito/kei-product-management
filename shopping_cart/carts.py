from .models import Cart, CartItem, AnonymousCart

def get_cart(request):
    if not request.session.exists(request.session.session_key):
        request.session.create() 
    cart_id = request.session.get('shopping_cart', -1)
    if request.user.is_authenticated:
        if int(cart_id) < 0:
            cart_object = Cart.objects.create(user=request.user)
            cart_id = cart_object.id
        else :
            cart_object = Cart.objects.get(id=cart_id)    
    else:
        if int(cart_id) < 0:
            cart_object = AnonymousCart.objects.create(anon_user=request.session.session_key)
            cart_id = cart_object.id
        else :
            cart_object =AnonymousCart.objects.get(id=cart_id)    

    request.session['shopping_cart'] = cart_id
    return {'cart_object':cart_object,'cart_id':cart_id}

def transfer_cart(request,key):
    pass
