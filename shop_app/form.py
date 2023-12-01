# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from shop_app.models import Customer


class CustomUserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta():
        model = User
        fields = ['username','first_name','last_name','email','password']


class Userprofile(forms.ModelForm):
    class Meta():
        model = Customer
        fields = ['phone']
