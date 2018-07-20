from django import forms
from shopping_cart.models import Cart, CartItem

class ProductCartForm (forms.Form):
    quantity = forms.IntegerField(required=True, initial=1)

    def __init__(self, *args, **kwargs):
        super(ProductCartForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['style'] = 'width:70px'
        self.fields['quantity'].widget.attrs['onChange'] = 'quantityChange()'