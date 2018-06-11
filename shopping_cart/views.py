from django.shortcuts import render

def get_total_items_in_cart(cart): #cart object
    total_amount = 0
    if cart.item_in_cart_set.all():
        for i in cart.item_in_cart_set.all():
            total_amount += i.quantity
        return total_amount
    else:
        return total_amount

def get_total_price(cart): #cart object
    total_amount = 0
    if cart.item_in_cart_set.all():
        for i in cart.item_in_cart_set.all():
            total_amount += i.quantity * i.product.price
        return total_amount
    else:
        return total_amount