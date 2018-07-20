from .models import WishList, WishListItem, AnonymousWishlist

def get_wishlist(request):
    if not request.session.exists(request.session.session_key):
        request.session.create() 
    wishlist_id = request.session.get('wishlist', -1)
    if request.user.is_authenticated:
        if int(wishlist_id) < 0:
            wishlist_object = WishList.objects.create(user=request.user)
            wishlist_id = wishlist_object.id
        else :
            wishlist_object = WishList.objects.get(id=wishlist_id)    
    else:
        if int(wishlist_id) < 0:
            wishlist_object = AnonymousWishlist.objects.create(anon_user=request.session.session_key)
            wishlist_id = wishlist_object.id
        else :
            wishlist_object = AnonymousWishlist.objects.get(id=wishlist_id)    

    request.session['wishlist'] = wishlist_id
    return {'wishlist_object':wishlist_object,'wishlist_id':wishlist_id}

def transfer_wishlist(request,key):
    pass
