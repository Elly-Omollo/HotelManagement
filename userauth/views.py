from django.contrib.auth import authenticate, login, logout
from userauth.forms import  UserRegistrationForm
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer, User, Profile
from django.contrib import messages

# Create your views here.


# customer login
def user_login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            # request.session['username'] = username
            # request.session['type'] = 'customer'
            messages.success(request, 'You are logged in succesfuly')
            return redirect('/customer/customer_dashboard.html/')
            # next_url = request.GET.get("next", "hotel:index")
            # return redirect(next_url)
        else:
            # print("==========Dear=======",email, "login failed please try again")
            messages.warning(request, "Invalid credential. Please try again.")
            return redirect('userauth:user_login')
            # return  render (request,'userauth/user_login.html',{})
        
    return render(request,'userauth/user_login.html',{})
    
# customer register
def user_signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        if Customer.objects.filter(username=username) or Customer.objects.filter(email=email):
           print(username , "already exist")
           messages.warning(request,"Account already exist, please choose a different username")
        else:
            password=request.POST['password']
            # otp=request.POST['otp']
            phone_no=request.POST['phone_no']
            # state=request.POST['state']
            error=[]
            if(len(username)<3):
                error.append(1)
                messages.warning(request,"Username Field must be greater than 3 character.")
            if(len(password)<5):
                error.append(1)
                messages.warning(request,"Password Field must be greater than 5 character.")
            if(len(email)==0):
                error.append(1)
                messages.warning(request,"Email field can't be empty")
            if(len(phone_no)!=10):
                error.append(1)
                messages.warning(request,"Valid Phone number is a 10 digit-integer.")
            if(len(error)==0):
                password_hash = make_password(password)
                customer=Customer(username=username,password=password_hash,email=email,phone_no=phone_no)
                customer.save()
                messages.info(request,"Account Created Successfully, please Login to continue")
                print("========== acount created successfully =========")
                redirect('hotel:index')
            else:
                print("===========",username, email, phone_no, "was not created")
                redirect('userauth:user_signup')
        
    else:
        pass
        # redirect('user_login')
    return render(request,'userauth/user_login.html',{})    




# manager signup page
def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already logged in." )
        return redirect("manager_dashboard")
    form = UserRegistrationForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get("full_name") 
        phone = form.cleaned_data.get("phone")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")


        user = authenticate(email=email, password=password)
        login(request, user)

        messages.success(request, f"hey {full_name}, your account has been created successfully.")

        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        return redirect("hotel:index")
    

    context = {
        "form":form
    }
    return render(request, "userauth/manager_signup.html", context)


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
 

def manager_login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are alredy logged in')
        return redirect("hotel:index")
    
    if request == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_query = User.objects.get(email=email)
            user_auth = authenticate(request, email=email, password=password)

            if user_query is not None:
                login(request, user_auth)
                messages.success(request, 'you are logged in')
                next_url = request.GET.get("next", "hotel:index")
                return redirect(next_url)
            else:
                messages.error(request, "Username or Passowrd doest not exist")
                return redirect("hotel:index")

        except:
            messages.error(request,'User doest not exist')
            return redirect('userauth:manager_login')
        

    return render(request, 'userauth/manager_login.html', {})
        

def logoutView(request):
    logout(request)
    messages.success(request, "You have longed out successfully")
    return redirect("userauth:manager_login")
    