from django import template

register = template.Library()

@register.filter
def int_to_kilogram(value):
    return '{:,}'.format(value/1000).replace(",",".")