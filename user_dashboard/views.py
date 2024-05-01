from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import models
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from django.conf import settings
from django.contrib import messages


from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# from paypal.standard.forms import PayPalPaymentsForm
from .models import  OrderModel, MenuItem


from user_dashboard.forms import AddHotelForm, AddRoomForm, AddRoomTypeForm, HotelForm
from user_dashboard.models import MenuItem, OrderModel
from hotel.models import  Hotel, Notification, Booking
from userauth.models import Profile, User
from userauth.forms import UserUpdateForm, ProfileUpdateForm
from .mails import order_email

# Create your views here.
@login_required
def home(request):
   profile = Profile.objects.get(user=request.user)
   appetizers = MenuItem.objects.filter(category__name__icontains='Appetizer')
   drinks = MenuItem.objects.filter(category__name__icontains='Drink')
   entre = MenuItem.objects.filter(category__name__icontains='Entre')
   fruit = MenuItem.objects.filter(category__name__icontains='Fruit')

   context = {
       'profile':profile,
       'appetizers': appetizers,
       'drinks': drinks,
       'entre': entre,
       'fruit': fruit
   }
   
   
   return render(request, 'user_dashboard/home.html', context)

# this is the user dashboard view
@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    bookings = Booking.objects.filter(username=request.user, payment_status="PAID")
    total_spent = Booking.objects.filter(username=request.user, payment_status="PAID").aggregate(amount=models.Sum("payable"))
    context ={
        "profile":profile,
        "bookings":bookings,
        "total_spent":total_spent
    }
    return render(request, 'user_dashboard/dashboard1.html', context)

@login_required
def booking_details(request, bookingid):
    profile = Profile.objects.get(user=request.user)
    booking = Booking.objects.get(bookingid=bookingid, username=request.user, payment_status="PAID")

    context = {
        "profile":profile,
        "booking":booking
    }
    return render(request, 'user_dashboard/booking_details.html', context)


@login_required
def bookings(request):
    profile = Profile.objects.get(user=request.user)
    bookings = Booking.objects.filter(username=request.user, payment_status="PAID")
    
    context = {
        "profile":profile,
        "bookings":bookings
    }
    return render(request, 'user_dashboard/bookings.html', context)

@login_required
def notifications(request):
    profile = Profile.objects.get(user=request.user)
    notifications = Notification.objects.filter(user=request.user, seen=False)

    context = {
        "profile":profile,
        "notifications":notifications
    }
    return render(request, "user_dashboard/notifications.html", context)


def notification_seen(request, id):
    noti = Notification.objects.get(id=id)
    noti.seen = True
    noti.save()
    messages.success(request, "Notification Seen!!")

    return redirect("user_dashboard:notifications")

@login_required
def wallet(request):
    profile = Profile.objects.get(user=request.user)
    bookings = Booking.objects.filter(username=request.user, payment_status="PAID")
    total_spent = Booking.objects.filter(username=request.user, payment_status="PAID").aggregate(amount=models.Sum("payable"))
    wallet_balance = request.user.profile.wallet
    context ={
        "profile": profile,
        "bookings":bookings,
        "total_spent":total_spent,
        "wallet_balance":wallet_balance
    }
    return render(request, 'user_dashboard/wallet.html', context)


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method=="POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect("user_dashboard:profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "profile":profile,
        "u_form":u_form,
        "p_form":p_form,
    }
    return render(request, "user_dashboard/profile.html", context)

# password change
@login_required
def password_changed(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "user_dashboard/password_changed.html",{'profile':profile})





# manager dashboard
@login_required
def add_hotel(request):
    profile = Profile.objects.get(user=request.user)
    room_form =AddRoomForm()
    roomtype_form = AddRoomTypeForm()
    if request.method == 'POST':
        form = AddHotelForm(request.POST, request.FILES)
        if form.is_valid():
            messages.info(request, "One hotel has been added successfuly")
            form.save()
            return redirect('user_dashboard:add_hotel')  # Redirect to a success page after adding the hotel
    else:
        # form = HotelForm()
        form = AddHotelForm()
    # if request.method == 'POST':
    #     form = HotelForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('user_dashboard:add_hotel')  
    # else:
    #     form = HotelForm()
    context = {
        "profile":profile,
        "form":form,
        "room_form":room_form,
        "roomtype_form":roomtype_form,
    }    

    return render(request, "user_dashboard/add-hotel.html", context)

# edit hotel view
@login_required
def edit_hotel(request):
    profile = Profile.objects.get(user=request.user)
    hotel = Hotel.objects.filter(full_name=request.user)
    allhotel=[]
    if request.method == 'POST':
        mh=get_object_or_404(Hotel, hotel_id=request.POST.get('hotel_id'))
        form = HotelForm(request.POST, request.FILES, instance=mh)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard:edit_hotel')  # Redirect to the dashboard after editing the hotel
    else:
        for h in hotel:
            allhotel.append(HotelForm( instance=h ))
            
        
    return render(request, 'user_dashboard/edit-hotel.html', {'form': allhotel, 'hotel': hotel,'profile':profile})
# end of manager dashboard 


#########pay pal ipin
def paypal_ipn_view(request):
    # Your PayPal IPN handling logic here
    return HttpResponse(status=200)












@login_required
def Order(request):
    profile = Profile.objects.get(user=request.user)

    #get all the items from every category
    appetizers = MenuItem.objects.filter(category__name__icontains='Appetizer')
    # appetizers = MenuItem.objects.all()
    drinks = MenuItem.objects.filter(category__name__icontains='Drink')
    entre = MenuItem.objects.filter(category__name__icontains='Entre')
    fruit = MenuItem.objects.filter(category__name__icontains='Fruit')

    #geting the food available in the menu
    details = User.objects.all()
    

    context = {
        'profile':profile,
        'appetizers':appetizers,
        'drinks':drinks,
        'entre':entre,
        'fruit': fruit, 
        'details': details
    }

    return render(request, 'user_dashboard/order1.html', context)

@csrf_exempt
def order_confirmation(request):
    profile = Profile.objects.get(user=request.user)
    #items from the post form
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        room_number = request.POST['room_number']
        room_type = request.POST['room_type']
        
        order_items = {
            'items': []
        }
        items = request.POST.getlist('items[]')
        item_ids = []
        price = 0
        # print("==========items1111", items, "=======")
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id':menu_item.pk,
                'name': menu_item.name,
                'price':menu_item.price
            }
            item_ids.append(menu_item.pk)
            # print("==========items2", item, "=======", item_data)
            order_items['items'].append(item_data)

            
            price += menu_item.price
        # item_ids = []
        # for items in order_items['items']:
        #     price += items['price']
        #     item_ids.append(item)
            # item_ids.append(item['id'])
        # print("IDS ->",item_ids)

        # return redirect('/user_dashboard/order_confirmation')
    
    order = OrderModel.objects.create(
        price=price,
        name=name,
        email=email,
        room_type = room_type,
        room_number = room_number
    )
    order.items.add(*item_ids)

    # send confirmation email
        
    # body = ('thank you for your order! Your food is being made and will be delivered soon! \n'
    #         f'Your total: {price}\n'
    #         'Thank you again for your order!')
    # send_mail(
    #     'Thank You for Your Order!',
    #     body,
    #     'ebooking@shahibu.com',
    #     [email],
    #     fail_silently=False
    # )

    subject = "Order Confirmation"
    message = f"""
                Hi {name}, Thank you for your order
                Your total is : {price}\n'
                Your food is being made and will be delivered soon!
            """
    sender = "ebooking@shahibu.com"
    receiver = [email]
    order_email(message, subject, receiver)
    # send_mail(
    #     subject,
    #     message,
    #     sender,
    #     receiver,
    #     fail_silently=False
    # )

    
    
    print("this is the order========", order_items['items'])
   
    context = {
        'profile':profile,
        'pk': order.pk,
        'items': order_items['items'],
        'price': price
    }

    # return redirect('user_dashboard:orderpay', pk=order.pk) 
    return render(request, 'user_dashboard/order_confirmation.html', context )



def orderpaid(request):
    return render(request, 'user_dashboard/orderpaid.html')