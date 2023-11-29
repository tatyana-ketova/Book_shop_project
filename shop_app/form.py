# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from shop_app.models import Customer


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last name'}))
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email id'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter user name'}))
    class Meta():
        model = User
        fields = ['username','first_name','last_name','email','password']


class Userprofile(forms.ModelForm):
    class Meta():
        model = Customer
        fields = ['phone']
