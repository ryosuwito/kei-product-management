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
from shopping_cart import carts, wishlists
from reward_system.models import Reward

import random
# Create your views here.

def login_page(request):   
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    welcome_message = ""
    try :
        if 'cart' in request.META['HTTP_REFERER']:
            welcome_message = "Login untuk Menyelesaikan Pembayaran"
    except:
        pass

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
                anon_cart = carts.get_cart(request)['cart_object']
                anon_wishlist = wishlists.get_wishlist(request)['wishlist_object']
                login(request, user)
                transfer_cart = carts.transfer_cart(request, anon_cart)
                transfer_wishlist= wishlists.transfer_wishlist(request, anon_wishlist)
                cart = transfer_cart['cart_object']
                wishlist = transfer_wishlist['wishlist_object']
                try :
                    if request.GET.get('next'):
                        return HttpResponseRedirect(request.GET.get('next'))
                except :
                    pass
                return HttpResponseRedirect(reverse('membership:profile'))
            else:
                form_messages='username atau password salah'
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('membership:profile'))
        form = MemberLoginForm()

    next = request.GET.get('next') if request.GET.get('next') else False
    return render(request, 'membership/login.html',
        {'wishlist': wishlist_object,
        'cart': cart_object,
        'next': next,
        'form': form, 
        'form_messages': form_messages,
        'welcome_message': welcome_message})

def pre_register_page(request, *args, **kwargs):
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    referal_code = False
    link = {
        'member': reverse('membership:register', current_app='member_backend'),
        'guest': reverse('membership:register', current_app='guest_backend'),
    }
    if request.get_host() != settings.DEFAULT_HOST:
        referal_code = check_host(request, pass_variable=True)
        if not referal_code:
            return  HttpResponseRedirect(request.scheme+"://"+settings.DEFAULT_HOST + 
                        reverse('membership:pre_register', 
                            current_app=request.resolver_match.namespace))
    else:
        try:
            referal_code = kwargs['referal_code'].lower()    
            if referal_code:
                link = {
                    'member': reverse('membership:register', current_app='member_backend', kwargs={'referal_code':referal_code.lower()}),
                    'guest': reverse('membership:register', current_app='guest_backend', kwargs={'referal_code':referal_code.lower()}),
                }
        except:
            pass

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('membership:profile'))

    next = request.GET.get('next') if request.GET.get('next') else False
    return render(request, 'membership/pre_register.html', 
        {'link':link, 
        'wishlist': wishlist_object,
        'cart': cart_object,
        'next':next})

def register_page(request, *args, **kwargs): 
    cart = carts.get_cart(request)
    cart_object = cart['cart_object']
    wishlist = wishlists.get_wishlist(request)
    wishlist_object = wishlist['wishlist_object']
    threshold = ''
    referal_code = False
    link_cancel = reverse('membership:pre_register', 
                            current_app=request.resolver_match.namespace)

    if request.get_host() != settings.DEFAULT_HOST:
        referal_code = check_host(request, pass_variable=True)
        if not referal_code:
            return  HttpResponseRedirect(request.scheme+"://"+settings.DEFAULT_HOST + 
                        reverse('membership:register', 
                            current_app=request.resolver_match.namespace))
    else:
        try:
            referal_code = kwargs['referal_code'].upper()
        except:
            pass

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('membership:profile'))
        
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
            """
            */ alamat utama untuk pendaftaran member / guest
            */ disimpan di field ktp_address
            */ alamat ini akan digunakan untuk tujuan pengiriman default
            */ bagi user tipe guest, alamat berupa home_address
            """
            response = render(request, 'membership/register_%s.html'%(namespace),
                            {'form': form, 'threshold': threshold, 'link_cancel':link_cancel})

            if namespace != 'guest':
                try :
                    """
                    */ cek apakah semua field lengkap, jika tidak kembalikan form 
                    """
                    if request.POST['provinsi'] and request.POST['kota'] and \
                    request.POST['kecamatan'] and request.POST['kelurahan'] :
                        provinsi = Provinsi.objects.get(pk=request.POST['provinsi']).name
                        kota = Kota.objects.get(pk=request.POST['kota']).name
                        kecamatan = Kecamatan.objects.get(pk=request.POST['kecamatan']).name
                        kelurahan = Kelurahan.objects.get(pk=request.POST['kelurahan']).name
                    else :
                        return response
                except :
                    return response
            else :
                try :
                    """
                    */ cek apakah semua field lengkap, jika tidak kembalikan form 
                    """
                    if request.POST['provinsi_home'] and request.POST['kota_home'] and \
                    request.POST['kecamatan_home'] and request.POST['kelurahan_home']:
                        pass
                    else :
                        return response
                except :
                    return response

            """
            */ alamat alternatif untuk pendaftaran member
            */ disimpan di field home_address
            */ alamat ini akan digunakan jika alamat rumah berbeda dengan alamat ktp
            """
            try :
                """
                */ cek apakah semua field lengkap, jika tidak kosongkan alamat rumah
                """
                if request.POST['provinsi_home'] and request.POST['kota_home'] and \
                request.POST['kecamatan_home'] and request.POST['kelurahan_home']:
                    provinsi_home = Provinsi.objects.get(pk=request.POST['provinsi_home']).name
                    kota_home = Kota.objects.get(pk=request.POST['kota_home']).name
                    kecamatan_home = Kecamatan.objects.get(pk=request.POST['kecamatan_home']).name
                    kelurahan_home = Kelurahan.objects.get(pk=request.POST['kelurahan_home']).name
            except :        
                provinsi_home = ''
                kota_home = ''
                kecamatan_home = ''
                kelurahan_home = ''

            """
            */ Buat akun user baru dengan data yang diberikan pengguna
            """
            username = data.get('username').lower()
            if User.objects.filter(username=username).count():
                raise forms.ValidationError(u'Username "%s" telah digunakan.' % username)
                
            password = data.get('password')
            email = data.get('email')
            user = User.objects.create_user(username=username, email=email, password=password)

            """
            */ Pisahkan nama menjadi first name dan last name
            """
            full_name = data.get('first_name').split(' ')
            user.last_name = full_name[-1] 
            user.first_name = ' '.join([x for x in full_name[:-1]])

            """
            */ Dapatkan kode sponsor jika tidak ada berikan kode referal acak
            """
            if referal_code:
                user.member.sponsor_code = referal_code
                user.member.sponsor = Member.objects.get(referal_code=referal_code).user
            else :
                sponsor_user = random.choice(User.objects.all())
                while sponsor_user.member.member_type == Member.GUEST :
                    sponsor_user = random.choice(User.objects.all())                  
                user.member.sponsor_code = sponsor_user.member.referal_code
                user.member.sponsor = sponsor_user

            """
            */ Tipe member pengguna yang baru daftar
            """
            if namespace == 'guest':
                user.member.member_type = 0
            else:
                user.member.member_type = data.get('member_type')      
               
            """
            */ Masukan data-data pengguna
            """         
            user.member.ktp_number = data.get('ktp_number')   
            user.member.bank_name = data.get('bank_name')          
            user.member.bank_account_number = data.get('bank_account_number')  
            user.member.bank_book_photo = data.get('bank_book_photo')
            user.member.ktp_photo = data.get('ktp_photo')
            user.member.phone_number = data.get('phone_number')          

            if namespace != 'guest':
                user.member.ktp_provinsi = provinsi
                user.member.ktp_kota = kota
                user.member.ktp_kecamatan = kecamatan
                user.member.ktp_kelurahan = kelurahan
                user.member.ktp_address = data.get('ktp_address')
    
            if data.get('home_address'):                 
                user.member.home_provinsi = provinsi_home
                user.member.home_kota = kota_home
                user.member.home_kecamatan = kecamatan_home
                user.member.home_kelurahan = kelurahan_home
                user.member.home_address = data.get('home_address')
            else :      
                user.member.copy_address()
                
            user.save()
            reward = Reward(member=user.member)
            if user is not None:
                anon_cart = carts.get_cart(request)['cart_object']
                anon_wishlist = wishlists.get_wishlist(request)['wishlist_object']
                logout(request)
                login(request, user)
                transfer_cart = carts.transfer_cart(request, anon_cart)
                transfer_wishlist= wishlists.transfer_wishlist(request, anon_wishlist)
                cart = transfer_cart['cart_object']
                wishlist = transfer_wishlist['wishlist_object']

                reward = Reward(member=user.member)
                reward.save()
                next = request.GET.get('next') if request.GET.get('next') else False
                if next :
                    return HttpResponseRedirect(next)
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
            'class': 'input-text',
            'style': 'width:100%'
            })
    return render(request, 'membership/register_%s.html'%(namespace),
        {'form': form, 
         'wishlist': wishlist_object,
         'cart': cart_object,
         'threshold': threshold, 
         'link_cancel':link_cancel})

@login_required(login_url='/member/login')
def profile_page(request, uname='none'):
    target = 0
    current_target = 0
    member_target = 0
    cart = carts.get_cart(request)['cart_object']
    wishlist = wishlists.get_wishlist(request)['wishlist_object']
    referal_code = False
    default_host = settings.DEFAULT_HOST 
    default_register_page = request.scheme+"://"+ default_host + \
                                reverse('membership:profile', 
                                    current_app=request.resolver_match.namespace)

    if request.get_host() != settings.DEFAULT_HOST:
        referal_code = check_host(request, pass_variable=True)
        if not referal_code:
            return  HttpResponseRedirect(default_register_page) 
                        
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

    if user.member.get_member_type_display() != 'Guest':
        current_target = user.member.reward.get_current_purchasing()
        current_selling_target = user.member.reward.get_current_selling()
        member_target = user.member.get_level()['TARGET']
        member_selling_target = user.member.get_level()['TARGET']
        target = round(current_target/member_target*100, 2)
        selling_target = round(current_selling_target/member_selling_target*100, 2)
        user.member.reward.get_purchasing_bonus(request)
        user.member.reward.get_selling_bonus(request)

    link_sponsor = ''
    if user.member.sponsor:
        sponsor = Member.objects.get(referal_code = user.member.sponsor_code)
        link_sponsor = sponsor.get_absolute_url()

    return render(request, 'membership/profile_member.html',
        {'user': user, 
        'target': target,
        'current_target': current_target,
        'member_target': member_target,
        'selling_target': selling_target,
        'current_selling_target': current_selling_target,
        'member_selling_target': member_selling_target,
        'cart':cart, 
        'default_host':default_host,
        'wishlist':wishlist,
        'link_edit': link_edit, 
        'link_sponsor': link_sponsor})

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
    namespace = request.resolver_match.namespace.split('_')[0].lower()
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

                    provinsi = Provinsi.objects.get(pk=request.POST['provinsi']).name
                    kota = Kota.objects.get(pk=request.POST['kota']).name
                    kecamatan = Kecamatan.objects.get(pk=request.POST['kecamatan']).name
                    kelurahan = Kelurahan.objects.get(pk=request.POST['kelurahan']).name
                    is_complete = True
            except :
                pass


            user = request.user
            
            if data.get('home_address') and is_complete:
                home_address = data.get('home_address')
                user.member.home_address = home_address
                user.member.home_provinsi = provinsi
                user.member.home_kota = kota
                user.member.home_kecamatan = kecamatan
                user.member.home_kelurahan = kelurahan

            if data.get('instagram_address') :
                user.member.instagram_address = data.get('instagram_address')
            if data.get('facebook_address') :
                user.member.facebook_address = data.get('facebook_address')
            if data.get('twitter_address') :
                user.member.twitter_address = data.get('twitter_address')
            if data.get('website_address') :
                user.member.website_address = data.get('website_address')
            if data.get('whatsapp_number') :
                user.member.whatsapp_number = data.get('whatsapp_number')

            if data.get('bank_book_photo') :
                user.member.bank_book_photo = data.get('bank_book_photo')
            if data.get('ktp_photo') :
                user.member.ktp_photo = data.get('ktp_photo')        
            if data.get('profile_photo') :
                user.member.profile_photo = data.get('profile_photo')       
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
