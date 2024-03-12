from django.contrib.auth import authenticate

from django.contrib import auth
from userauth.forms import  UserRegistrationForm
from django.shortcuts import redirect, render

from django.contrib.auth.hashers import make_password, check_password
from .models import  User, Profile
from django.contrib import messages

# Create your views here.


# manager signup page
def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already logged in." )
        return redirect("hotel:index")
    form = UserRegistrationForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get("full_name") 
        phone = form.cleaned_data.get("phone")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")


        user = authenticate(email=email, password=password)
        # login(request, user)
        auth.login(request, user)

        messages.success(request, f"hey {full_name}, your account has been created successfully.")

        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        return redirect("hotel:index")
    
   

    context = {
        "form":form
    }
    return render(request, "userauth/signup.html", context)


# def manager_login(request):
#     if request.method=='POST':
#         username=request.POST['username']
#         passwd=request.POST['password']
#         user=auth.authenticate(username=username, password=passwd)
#         if user is not None:
#             auth.login(request,user)
#             return redirect('/manager_dashboard')
#         messages.warning(request,'Invalid logins')
#         return redirect(RegisterView)
#     else:
#         return render(request, 'userauth/manager_login.html')
 

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are alredy logged in')
        # return redirect("hotel:index")
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_query = User.objects.get(email=email)
            user_auth = authenticate(request, email=email, password=password)

            if user_query is not None:
                auth.login(request, user_auth)
                messages.success(request, 'you are logged in')
                next_url = request.GET.get("next", "hotel:index")
                return redirect(next_url)
            else:
                messages.error(request, "Username or Passowrd doest not exist")
                return redirect("hotel:index")

        except:
            messages.error(request,'User doest not exist')
            return redirect('userauth:login')
        

    return render(request, 'userauth/login.html', {})
        

def logoutView(request):
    auth.logout(request)
    messages.success(request, "You have longed out successfully")
    return redirect("userauth:login")
    