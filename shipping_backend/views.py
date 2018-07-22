from django.http import HttpResponse
from django.shortcuts import render
from .shipping_check import get_province as province
from .shipping_check import get_province_id as province_id
from .shipping_check import get_city_id as city_id
from .shipping_check import get_city as city
from .shipping_check import get_cost as cost

def get_province(request):
    return HttpResponse(province())

def get_province_id(request):
    return HttpResponse(province_id('Papua Barat'))

def get_city(request):
    return HttpResponse(city())

def get_city_id(request):
    return HttpResponse(city_id('3', 'Kabupaten Tangerang'))

def get_cost(request):
    return HttpResponse(cost(request.user, 'tiki'))