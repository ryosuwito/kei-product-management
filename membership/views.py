from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User 
from django.urls import reverse
from django.db.models import Q
from .models import Member
from .forms import MemberLoginForm, MemberRegisterForm, GuestRegisterForm
# Create your views here.

def login_page(request):
    form_messages=''
    if request.method == 'POST':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('membership:profile'))
        form = MemberLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username,
                password=password)
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
            return HttpResponseRedirect(reverse('membership:profile'))
        form = MemberLoginForm()
    return render(request, 'membership/login.html',{'form': form, 'form_messages': form_messages})

def pre_register_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('membership:profile'))
    link = {
        'member': reverse('membership:register', current_app='member_backend'),
        'guest': reverse('membership:register', current_app='guest_backend'),
    }
    return render(request, 'membership/pre_register.html', {'link':link})

def register_page(request):  
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('membership:profile'))
    referal_code = False
    threshold = ''
    namespace = reverse('membership:register', 
        current_app=request.resolver_match.namespace).split('/')[1]
    if namespace != 'guest':
        threshold = {k: v for k,v in Member.LEVEL.items() if k != 'MASTER_SELLER'}
    if request.get_host() != 'localhost':
        userref = request.get_host().split('.')
        try :
            user = User.objects.get(username=userref[0])
        except :
            user = False
        if user :
            referal_code = user.member.referal_code

    if request.method == 'POST':
        if namespace == 'guest':
            form = GuestRegisterForm(request.POST)
        else:
            form = MemberRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username').lower()
            password = data.get('password')
            email = data.get('email')
            
            user = User.objects.create_user(username=username, email=email, password=password)
            full_name = data.get('first_name').split(' ')
            user.last_name = full_name[-1] 
            user.first_name = ' '.join([x for x in full_name[:-1]])
            if referal_code:
                user.member.sponsor_code = referal_code
                user.member.sponsor = Member.objects.get(referal_code=referal_code).user
            if namespace == 'guest':
                user.member.member_type = 0
            else:
                user.member.member_type = data.get('member_type')
            
            user.member.phone_number = data.get('phone_number')            
            user.member.ktp_number = data.get('ktp_number')           
            user.member.bank_account_number = data.get('bank_account_number')  
            user.member.bank_book_photo = data.get('bank_book_photo')
            user.member.ktp_photo = data.get('ktp_photo')              
            user.member.ktp_address = data.get('ktp_address')
            if data.get('home_address'):                 
                user.member.home_address = data.get('home_address')
            
            user.save()
            if user is not None:
                logout(request)
                login(request, user)
                return HttpResponseRedirect(reverse('membership:profile', 
                    current_app=request.resolver_match.namespace))
            else:
                return HttpResponse("Create User Fail")
    elif request.method == 'GET': 
        if namespace == 'guest':
            form = GuestRegisterForm()
        else:
            form = MemberRegisterForm()
        if referal_code:
            form.fields['sponsor_code'].default = referal_code
            form.fields['sponsor_code'].initial = referal_code
            form.fields['sponsor_code'].disabled = True
            form.fields['sponsor_code'].widget.attrs.update({
            'class': 'sponsor-disabled'
            })
    return render(request, 'membership/register_%s.html'%(namespace),
        {'form': form, 'threshold': threshold})

@login_required(login_url='/member/login')
def profile_page(request, pk=0):
    namespace = reverse('membership:register', 
        current_app=request.resolver_match.namespace).split('/')[1]
    if pk == 0 or pk == request.user.pk :
        if request.user.member.get_member_type_display() == 'guest' and \
                request.resolver_match.namespace != 'guest_backend':
            return HttpResponseRedirect(reverse('membership:profile', 
                current_app='guest_backend'))
        user = request.user
    else :
        user = get_object_or_404(User, pk=pk)
        if user.member.get_member_type_display() != 'guest' and \
                request.resolver_match.namespace != 'member_backend':
            return HttpResponseRedirect("%s%s"%(reverse('membership:profile', 
                current_app='member_backend'),pk))
    return render(request, 'membership/profile_%s.html'%(namespace),{'user': user})

def log_check(user):
    return user.is_authenticated

@user_passes_test(log_check)
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('membership:login', 
        current_app=request.resolver_match.namespace))