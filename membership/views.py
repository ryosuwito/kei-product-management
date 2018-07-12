from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User 
from django.urls import reverse
from django.db.models import Q
from database_wilayah.models import Provinsi, Kota, Kecamatan, Kelurahan
from .models import Member
from .forms import MemberLoginForm, MemberRegisterForm, GuestRegisterForm, MemberEditProfileForm
import random
# Create your views here.

def login_page(request):   
    referal_code = False
    if request.get_host() != settings.DEFAULT_HOST:
        referal_code = check_host(request, pass_variable=True)
        if not referal_code:
            return  HttpResponseRedirect(request.scheme+"://"+settings.DEFAULT_HOST + 
                        reverse('membership:login', 
                            current_app=request.resolver_match.namespace)) 
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
    referal_code = False
    if request.get_host() != settings.DEFAULT_HOST:
        referal_code = check_host(request, pass_variable=True)
        if not referal_code:
            return  HttpResponseRedirect(request.scheme+"://"+settings.DEFAULT_HOST + 
                        reverse('membership:pre_register', 
                            current_app=request.resolver_match.namespace))
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('membership:profile'))
    link = {
        'member': reverse('membership:register', current_app='member_backend'),
        'guest': reverse('membership:register', current_app='guest_backend'),
    }
    return render(request, 'membership/pre_register.html', {'link':link})

def register_page(request): 
    referal_code = False
    if request.get_host() != settings.DEFAULT_HOST:
        referal_code = check_host(request, pass_variable=True)
        if not referal_code:
            return  HttpResponseRedirect(request.scheme+"://"+settings.DEFAULT_HOST + 
                        reverse('membership:register', 
                            current_app=request.resolver_match.namespace))
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('membership:profile'))
    threshold = ''
    namespace = reverse('membership:register', 
        current_app=request.resolver_match.namespace).split('/')[1]
    if namespace != 'guest':
        threshold = {k: v for k,v in Member.LEVEL.items() if k != 'MASTER_SELLER'}

    if request.method == 'POST':
        if namespace == 'guest':
            form = GuestRegisterForm(request.POST)
        else:
            form = MemberRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            try :
                if request.POST['provinsi'] and request.POST['kota'] and \
                request.POST['kecamatan'] and request.POST['kelurahan']:

                    provinsi = data.get('provinsi')
                    kota = Kota.objects.get(pk=request.POST['kota'])
                    kecamatan = Kecamatan.objects.get(pk=request.POST['kecamatan'])
                    kelurahan = Kelurahan.objects.get(pk=request.POST['kelurahan'])

                else :
                    return render(request, 'membership/register_%s.html'%(namespace),
                        {'form': form, 'threshold': threshold})
            except :
                return render(request, 'membership/register_%s.html'%(namespace),
                    {'form': form, 'threshold': threshold})

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
            else :
                sponsor_user = random.choice(User.objects.all())
                user.member.sponsor_code = sponsor_user.member.referal_code
                user.member.sponsor = sponsor_user

            if namespace == 'guest':
                user.member.member_type = 0
            else:
                user.member.member_type = data.get('member_type')
            
            user.member.phone_number = data.get('phone_number')            
            user.member.ktp_number = data.get('ktp_number')           
            user.member.bank_account_number = data.get('bank_account_number')  
            user.member.bank_book_photo = data.get('bank_book_photo')
            user.member.ktp_photo = data.get('ktp_photo')                   
            if namespace == 'guest':    
                user.member.ktp_address = data.get('home_address') + ", %s, %s, %s, %s" % (kelurahan, kecamatan, kota, provinsi)
            else:
                user.member.ktp_address = data.get('ktp_address') + ", %s, %s, %s, %s" % (kelurahan, kecamatan, kota, provinsi)

            if data.get('home_address'):                 
                user.member.home_address = data.get('home_address')
            else :
                user.member.home_address = user.member.ktp_address
            
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
def profile_page(request, uname='none'):
    referal_code = False
    if request.get_host() != settings.DEFAULT_HOST:
        referal_code = check_host(request, pass_variable=True)
        if not referal_code:
            return  HttpResponseRedirect(request.scheme+"://"+settings.DEFAULT_HOST + 
                        reverse('membership:profile', 
                            current_app=request.resolver_match.namespace)) 
    namespace = request.resolver_match.namespace
    member_type = namespace.split('_')[0]
    link_edit = ''

    if uname == 'none' or uname == request.user.username :
        if request.user.member.get_member_type_display() != 'Guest' and \
            request.resolver_match.namespace != 'member_backend':     
                return HttpResponseRedirect(reverse('membership:profile', 
                    current_app='member_backend'))
        if request.user.member.get_member_type_display() == 'Guest' and \
            request.resolver_match.namespace != 'guest_backend':     
                return HttpResponseRedirect(reverse('membership:profile', 
                    current_app='guest_backend'))

        link_edit = reverse('membership:edit_profile', current_app=namespace)
        user = request.user
    else :
        user = get_object_or_404(User, username=uname)
        if user.member.get_member_type_display() != 'Guest' and \
                request.resolver_match.namespace != 'member_backend':
            return HttpResponseRedirect("%s%s"%(reverse('membership:profile', 
                current_app='member_backend'),uname))
        if user.member.get_member_type_display() == 'Guest' and \
                request.resolver_match.namespace != 'guest_backend':
            return HttpResponseRedirect("%s%s"%(reverse('membership:profile', 
                current_app='guest_backend'),uname))

    link_sponsor = ''
    if user.member.sponsor:
        sponsor = Member.objects.get(referal_code = user.member.sponsor_code)
        link_sponsor = sponsor.get_absolute_url()

    return render(request, 'membership/profile_%s.html'%(member_type),
        {'user': user, 'link_edit': link_edit, 'link_sponsor': link_sponsor})

@login_required(login_url='/member/login')
def edit_profile_page(request):
    referal_code = False
    if request.get_host() != settings.DEFAULT_HOST:
        referal_code = check_host(request, pass_variable=True)
        if not referal_code:
            return  HttpResponseRedirect(request.scheme+"://"+settings.DEFAULT_HOST + 
                        reverse('membership:edit_profile', 
                            current_app=request.resolver_match.namespace)) 
    provinsi = ''
    kota = ''
    kecamatan = ''
    kelurahan = ''
    home_address = ''
    is_complete = False
    namespace = reverse('membership:edit_profile', 
        current_app=request.resolver_match.namespace).split('/')[1]
    if request.method == 'POST':   
        if namespace == 'guest':          
            return HttpResponse("Edit Profile Fail")
        else:
            form = MemberEditProfileForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            try :
                if request.POST['provinsi'] and request.POST['kota'] and \
                request.POST['kecamatan'] and request.POST['kelurahan']:

                    provinsi = data.get('provinsi')
                    kota = Kota.objects.get(pk=request.POST['kota'])
                    kecamatan = Kecamatan.objects.get(pk=request.POST['kecamatan'])
                    kelurahan = Kelurahan.objects.get(pk=request.POST['kelurahan'])
                    is_complete = True
            except :
                pass


            user = request.user
            
            if data.get('home_address') and is_complete:
                home_address = data.get('home_address')
                user.member.home_address = home_address + ", %s, %s, %s, %s" % (kelurahan, kecamatan, kota, provinsi)

            if data.get('instagram_address') :
                user.member.instagram_address = data.get('instagram_address')
            if data.get('facebook_address') :
                user.member.facebook_address = data.get('facebook_address')
            if data.get('twitter_address') :
                user.member.twitter_address = data.get('twitter_address')
            if data.get('line_address') :
                user.member.line_address = data.get('line_address')
            if data.get('website_address') :
                user.member.website_address = data.get('website_address')
            if data.get('whatsapp_number') :
                user.member.whatsapp_number = data.get('whatsapp_number')

            if data.get('bank_book_photo') :
                user.member.bank_book_photo = data.get('bank_book_photo')
            if data.get('ktp_photo') :
                user.member.ktp_photo = data.get('ktp_photo')            
            if data.get('smart_motto') :
                user.member.smart_motto = data.get('smart_motto')               

            user.save()
            return HttpResponseRedirect(reverse('membership:profile', 
                current_app=request.resolver_match.namespace))

    elif request.method == 'GET': 
        if namespace == 'guest':
            form = MemberEditProfileForm()
        else:
            form = MemberEditProfileForm()
            if request.user.member.instagram_address:
                form.fields['instagram_address'].widget.attrs.update({
                'placeholder': request.user.member.instagram_address
                })
            if request.user.member.facebook_address:
                form.fields['facebook_address'].widget.attrs.update({
                'placeholder': request.user.member.facebook_address
                })
            if request.user.member.line_address:
                form.fields['line_address'].widget.attrs.update({
                'placeholder': request.user.member.line_address
                })
            if request.user.member.twitter_address:
                form.fields['twitter_address'].widget.attrs.update({
                'placeholder': request.user.member.twitter_address
                })
            if request.user.member.website_address:
                form.fields['website_address'].widget.attrs.update({
                'placeholder': request.user.member.website_address
                })
            if request.user.member.whatsapp_number:
                form.fields['whatsapp_number'].widget.attrs.update({
                'placeholder': request.user.member.whatsapp_number
                })
            if request.user.member.home_address != request.user.member.ktp_address:
                form.fields['home_address'].widget.attrs.update({
                'placeholder': request.user.member.home_address
                })

    return render(request, 'membership/edit_profile_%s.html'%(namespace),
        {'form': form})

def log_check(user):
    return user.is_authenticated

@user_passes_test(log_check)
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('membership:login', 
        current_app=request.resolver_match.namespace))

def check_host(request, pass_variable = False):
    referal_code = False
    userref = request.get_host().split('.')
    try :
        user = User.objects.get(username=userref[0])
    except :
        user = False
    if user :
        referal_code = user.member.referal_code
    elif pass_variable == True :            
        referal_code = False      
        #return
    return referal_code
