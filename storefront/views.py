from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from .forms import StoreLoginForm, StoreRegisterForm
# Create your views here.
def login_page(request):
    if request.method == 'POST':
        form = StoreLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("Login Success")
            else:
                return HttpResponse("No User")
        else:
            return render(request, 'storefront/login.html',{'form': form})
    elif request.method == 'GET':
        form = StoreLoginForm()
        return render(request, 'storefront/login.html',{'form': form})


def register_page(request):  
    if request.method == 'POST':
        form = StoreRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            user = User.objects.create_user(username=username, email=email, password=password)
            if user is not None:
                logout(request)
                login(request, user)
                return HttpResponse("Create User Success as : {}".format(user.username))
            else:
                return HttpResponse("Create User Fail")
        else:
            return render(request, 'storefront/daftar.html',{'form': form})
    elif request.method == 'GET':
        form = StoreRegisterForm()
        return render(request, 'storefront/daftar.html',{'form': form})