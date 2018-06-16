from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User 
from django.urls import reverse
from .forms import MemberLoginForm, MemberRegisterForm
# Create your views here.

def login_page(request):
    form_messages=''
    if request.method == 'POST':
        form = MemberLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try :
                    if request.GET['next']:
                        return HttpResponseRedirect(request.GET['next'])
                except :
                    return HttpResponseRedirect(reverse('membership:profile'))
            else:
                form_messages='username atau password salah'
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('membership:register'))
        form = MemberLoginForm()
    return render(request, 'membership/login.html',{'form': form, 'form_messages': form_messages})

def register_page(request):  
    referal_code = ''
    namespace = reverse('membership:register', current_app=request.resolver_match.namespace).split('/')[1]
    if request.get_host() != 'localhost':
        userref = request.get_host().split('.')
        try :
            user = User.objects.get(username=userref[0])
        except :
            user = False
        if user :
            referal_code = user.member.referal_code

    if request.method == 'POST':
        form = MemberRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username').lower()
            password = data.get('password')
            email = data.get('email')
            user = User.objects.create_user(username=username, email=email, password=password)
            user.member.sponsor_code = referal_code
            if namespace == 'guest':
                user.member.member_type = 0
            user.save()
            if user is not None:
                logout(request)
                login(request, user)
                return HttpResponse("Create User Success as : {}".format(user.username))
            else:
                return HttpResponse("Create User Fail")
        else:
            return render(request, 'membership/daftar.html',{'form': form})
    elif request.method == 'GET':
        form = MemberRegisterForm()
        form.fields['sponsor_code'].default = referal_code
        form.fields['sponsor_code'].initial = referal_code
        form.fields['sponsor_code'].disabled = True
        return render(request, 'membership/daftar.html',{'form': form})

@login_required(login_url='/member/login')
def profile_page(request, pk=0):
    namespace = reverse('membership:register', current_app=request.resolver_match.namespace).split('/')[1]
    if pk == 0 or pk == request.user.pk :
        if request.user.member.get_member_type_display() == 'guest' and \
                request.resolver_match.namespace != 'guest_backend':
            return HttpResponseRedirect(reverse('membership:profile', current_app='guest_backend'))
        user = request.user
    else :
        user = get_object_or_404(User, pk=pk)
        if user.member.get_member_type_display() != 'guest' and \
                request.resolver_match.namespace != 'member_backend':
            return HttpResponseRedirect("%s%s"%(reverse('membership:profile', current_app='member_backend'),pk))
    return render(request, 'membership/profile_%s.html'%(namespace),{'user': user})

def log_check(user):
    return user.is_authenticated

@user_passes_test(log_check)
def logout_page(request):
    logout(request)
    return HttpResponse("Logout Success")