from django import forms
from django.contrib.auth.models import User
from database_wilayah.models import Provinsi

class MemberLoginForm(forms.Form):
    username = forms.CharField(label='Username :', max_length=150)
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
    username = forms.CharField(required=True, min_length=USERNAME_MIN, max_length=USERNAME_MAX)
    sponsor_code = forms.CharField(min_length=12, max_length=12)
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
        fields = ('username', 'password','email')
        error_messages = {
            'username': {
                'required': 'Harap masukan username dengan benar',
                'max_length': 'Username telalu panjang, maksimal {}'.format(USERNAME_MAX),
                'min_length': 'Username telalu pendek, minimal {}'.format(USERNAME_MIN),
                'invalid': 'Username tidak boleh ada spasi. Hanya alfabet, angka dan karaker @/./+/-/'
            },
        }