from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
@login_required
def index(request):
    return HttpResponse('taik babik kau')

def checkout(request):
    pass

def history(request):
    pass