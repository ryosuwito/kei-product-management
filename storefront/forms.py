from django import forms
from django.contrib.auth.models import User

class StoreLoginForm(forms.Form):
    username = forms.CharField(label='Username :', max_length=150)
    attrs = {
        "type": "password"
    }
    password = forms.CharField(label='Password :', widget=forms.PasswordInput(attrs=attrs))

class StoreRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StoreRegisterForm, self).__init__(*args, **kwargs)

        # sets the placeholder key/value in the attrs for a widget
        # when the form is instantiated (so the widget already exists)
        self.fields['username'].widget.attrs['placeholder'] = 'Masukan Username'
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs['placeholder'] = '*********'
        self.fields['email'].widget = forms.EmailInput()
        self.fields['email'].widget.attrs['placeholder'] = 'Masukan Email Aktif'

    class Meta:
        model = User
        fields = ('username', 'password','email')