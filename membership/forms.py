from django import forms
from django.contrib.auth.models import User
from database_wilayah.models import Provinsi
from .models import Member

class MemberLoginForm(forms.Form):
    username = forms.CharField(label='Username/ Phone/ Email :', max_length=150)
    attrs = {
        "type": "password"
    }
    password = forms.CharField(label='Password :', widget=forms.PasswordInput(attrs=attrs))

class MemberRegisterForm(forms.ModelForm):
    USERNAME_MAX = 20
    USERNAME_MIN = 6
    error_messages = {
        'duplicate_username': 'Pengguna dengan username tersebut sudah ada'
    }
    
    provinsi = forms.ModelChoiceField(Provinsi.objects.all(), initial='')
    member_type = forms.ChoiceField(choices = Member.USER_TYPE_CHOICES[2:-1], initial=0, required=True)
    username = forms.CharField(required=True, min_length=USERNAME_MIN, max_length=USERNAME_MAX)
    phone_number = forms.CharField(required=True, max_length=17)
    sponsor_code = forms.CharField(min_length=12, max_length=12)
    ktp_address = forms.CharField(max_length=250, required=True)
    home_address = forms.CharField(max_length=250, required=False)
    ktp_number = forms.IntegerField(required=True)
    bank_account_number = forms.IntegerField(required=True)
    bank_book_photo = forms.ImageField(required=False) 
    ktp_photo = forms.ImageField(required=False)
    def __init__(self, *args, **kwargs):
        super(MemberRegisterForm, self).__init__(*args, **kwargs)

        # sets the placeholder key/value in the attrs for a widget
        # when the form is instantiated (so the widget already exists)
        self.fields['username'].widget.attrs['placeholder'] = 'Masukan Username'
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs['placeholder'] = '*********'
        self.fields['email'].widget = forms.EmailInput()
        self.fields['email'].widget.attrs['placeholder'] = 'Masukan Email Aktif'
        self.fields['sponsor_code'].required = False
        
        self.fields['provinsi'].widget.attrs['onClick'] = 'getKota()'

        self.fields['phone_number'].widget = forms.NumberInput()
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Contoh : +628129999999 / 0812999999'

        self.fields['ktp_number'].widget.attrs['placeholder'] = 'Contoh : 3671081xxxxxxxxxx'
        self.fields['ktp_number'].widget = forms.NumberInput()
        
        self.fields['bank_account_number'].widget.attrs['placeholder'] = 'Contoh : 7211XXCCCCCCDDF'
        self.fields['bank_account_number'].widget = forms.NumberInput()

        self.fields['ktp_address'].widget = forms.Textarea() 
        self.fields['ktp_address'].widget.attrs['rows'] = '3'
        self.fields['ktp_address'].widget.attrs['placeholder'] = 'Contoh: Jl. Angkasa 1 Blok AF6 NO 18'

        self.fields['home_address'].widget = forms.Textarea() 
        self.fields['home_address'].widget.attrs['rows'] = '3' 
        self.fields['home_address'].widget.attrs['placeholder'] = 'Contoh: Jl. Angkasa 1 Blok AF6 NO 18'

        self.fields['bank_book_photo'].widget.attrs['onChange'] = 'Handlechange(event, this.id)'
        self.fields['bank_book_photo'].widget.attrs['class'] = 'hidden'

        self.fields['ktp_photo'].widget.attrs['onChange'] = 'Handlechange(event, this.id)'
        self.fields['ktp_photo'].widget.attrs['class'] = 'hidden'

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
       
        try:
            User._default_manager.get(username=username)
            #if the user exists, then let's raise an error message

            raise forms.ValidationError( 
              self.error_messages['duplicate_username'],     #set the error message key
            )
        except User.DoesNotExist:
            return username # great, this user does not exist so we can continue the registration process

    class Meta:
        USERNAME_MAX = 20
        USERNAME_MIN = 6
        model = User
        fields = ('username', 'password','email', 'first_name')
        error_messages = {
            'username': {
                'required': 'Harap masukan username dengan benar',
                'max_length': 'Username telalu panjang, maksimal {}'.format(USERNAME_MAX),
                'min_length': 'Username telalu pendek, minimal {}'.format(USERNAME_MIN),
                'invalid': 'Username tidak boleh ada spasi. Hanya alfabet, angka dan karaker @/./+/-/'
            },
        }

class GuestRegisterForm(MemberRegisterForm):
    member_type = forms.ChoiceField(choices = Member.USER_TYPE_CHOICES[2:-1], initial=0, required=False)
    def __init__(self, *args, **kwargs):
        super(GuestRegisterForm, self).__init__(*args, **kwargs)

        # sets the placeholder key/value in the attrs for a widget
        # when the form is instantiated (so the widget already exists)
        self.fields['ktp_number'].required = False
        self.fields['bank_account_number'].required = False
        self.fields['phone_number'].required = False
        self.fields['ktp_address'].required = False
        self.fields['ktp_address'].required = False

class MemberEditProfileForm(forms.ModelForm):   
    instagram_address = forms.CharField(max_length=250, required=False)  
    facebook_address = forms.CharField(max_length=250, required=False)   
    twitter_address = forms.CharField(max_length=250, required=False)     
    line_address = forms.CharField(max_length=250, required=False)  
    website_address = forms.CharField(max_length=250, required=False)
    whatsapp_number = forms.CharField(required=False)

    home_address = forms.CharField(max_length=250, required=True)
    bank_book_photo = forms.ImageField(required=False) 
    ktp_photo = forms.ImageField(required=False)
    
    provinsi = forms.ModelChoiceField(Provinsi.objects.all(), initial='')  
    def __init__(self, *args, **kwargs):
        super(MemberEditProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['instagram_address'].widget.attrs['placeholder'] = 'contoh : @instagram123'
        self.fields['facebook_address'].widget.attrs['placeholder'] = 'contoh : https://www.facebook.com/fb123'
        self.fields['twitter_address'].widget.attrs['placeholder'] = 'contoh : @twitter123'
        self.fields['line_address'].widget.attrs['placeholder'] = 'contoh : @line123'
        self.fields['website_address'].widget.attrs['placeholder'] = 'contoh : https://www.blog.com/'
        self.fields['whatsapp_number'].widget = forms.NumberInput()

        self.fields['bank_book_photo'].widget.attrs['onChange'] = 'Handlechange(event, this.id)'
        self.fields['bank_book_photo'].widget.attrs['class'] = 'hidden'

        self.fields['ktp_photo'].widget.attrs['onChange'] = 'Handlechange(event, this.id)'
        self.fields['ktp_photo'].widget.attrs['class'] = 'hidden'
      
        self.fields['provinsi'].widget.attrs['onClick'] = 'getKota()'
        
        self.fields['home_address'].widget = forms.Textarea() 
        self.fields['home_address'].widget.attrs['rows'] = '3' 
        self.fields['home_address'].widget.attrs['placeholder'] = 'Contoh: Jl. Angkasa 1 Blok AF6 NO 18'

    class Meta:
        USERNAME_MAX = 30
        USERNAME_MIN = 4
        model = Member
        fields = ('instagram_address', 'facebook_address','twitter_address', 'line_address',\
                  'website_address', 'whatsapp_number', 'bank_book_photo', 'ktp_photo')
        error_messages = {
            'twitter_address': {
                'required': 'Harap masukan username dengan benar',
                'max_length': 'Username telalu panjang, maksimal {}'.format(USERNAME_MAX),
                'min_length': 'Username telalu pendek, minimal {}'.format(USERNAME_MIN),
                'invalid': 'Username tidak boleh ada spasi. Hanya alfabet, angka dan karaker @/./+/-/'
            },
        }
        
        
        