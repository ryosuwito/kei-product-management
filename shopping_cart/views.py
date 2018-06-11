from django.shortcuts import render

def get_total_items_in_cart(cart):
    total_amount = 0
    for i in cart.item_in_cart_set.all():
        total_amount += i.quantity
    return total_amount
