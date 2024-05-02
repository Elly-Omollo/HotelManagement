from django import forms
from django.forms import FileInput
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User, Profile
 
class UserRegistrationForm(UserCreationForm):

    full_name = forms.CharField(widget=forms.TextInput(attrs={ 'class':'form-group'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-group'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-group'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-group'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class':'form-group'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class':'form-group'}))
    
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


