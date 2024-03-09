from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User, Profile
 
class UserRegistrationForm(UserCreationForm):

    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Enter your name here"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Enter your username here"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Enter your Email here"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Enter your phone here"}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Enter your password here"}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Confirm your password"}))
    
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone', 'password1', 'password2']