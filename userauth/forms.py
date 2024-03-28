from django import forms
from django.forms import FileInput
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


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields =['email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "image",
            "full_name",
            "phone",
            "gender",
            "country",
            "city",
            "state",
            "address",
            "identity_type",
            "identity_image",
            "facebook",
            "twitter",
            "instagram"
        ]
        
        widgets = {
            "image": FileInput(attrs={"onchange": "loadFile(event)", "class":"upload"})
        }


