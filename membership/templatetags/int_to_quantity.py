from django import template

register = template.Library()

@register.filter
def int_to_quantity(value):
    return '{:,}'.format(value).replace(",",".")