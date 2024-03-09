from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from hotel.models import Coupon, Hotel, Room, RoomType, Booking,Activitylog

# Create your views here.

def index(request):
    hotels = Hotel.objects.filter(status="Live")
    roomtype = RoomType.objects.all()
    context ={
        "hotels":hotels,
        "roomtype":roomtype,
      
    }
  
    return render(request, "hotel/index.html", context)

def hotel_details(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    context ={
        "hotel":hotel,
    }
    return render(request, "hotel/hotel_details.html", context)


def room_type_details(request, slug, rt_slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    room_type = RoomType.objects.get(hotel=hotel, slug=rt_slug)
    rooms = Room.objects.filter(room_type=room_type, is_available=True)

    id = request.GET.get("hotel-id")
    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")
    adults = request.GET.get("adults")
    children = request.GET.get("children")

    print("These are the detsils that are from the selected rooms from room type details========")
    
    print("ID ========", id)
    print("this is the checkin date ========", checkin)
    print("chckout date ========", checkout)
    # print("adults ========", adults)
    # print(" children ========", children)
    # print(" hotel ========", hotel)
    # print(" room type ========", room_type)
    # print(" rooms ========", rooms)

    context = {
        "hotel":hotel,
        "room_type": room_type,
        "rooms":rooms,
        "checkin":checkin,
        "checkout":checkout,
        "adults":adults,
        "children":children,
    }

    return render(request, "hotel/room_type_details.html", context)


def selected_rooms(request):
    # these are the placeholdres variables
    total=0
    room_count=0
    total_days=0
    adults=0
    children=0
    checkin=""
    checkout=""


    if 'selection_data_obj' in request.session:
        if request.method == "POST":
            for h_id, item in request.session['selection_data_obj'].items():
                id = int(item['hotel_id'])
                checkin = item['checkin']
                checkout = item['checkout']
                adults = int(item['adults'])
                children = int(item['children'])
                room_type_ = int(item['room_type'])
                room_id = int(item['room_id'])

                user = request.user
                hotel = Hotel.objects.get(id=id)
                room = Room.objects.get(id=room_id)
                room_type = RoomType.objects.get(id=room_type_)

            date_format = "%Y-%m-%d"
            checkin_date = datetime.strptime(checkin, date_format)
            checkout_date = datetime.strptime(checkout, date_format)

            time_difference = checkout_date - checkin_date
            total_days = time_difference.days

            full_name = request.POST.get("full_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")

            booking = Booking.objects.create(
                # username = user,
                hotel=hotel,
                room_type=room_type,
                check_in_date=checkin,
                check_out_date=checkout,
                total_days=total_days,
                number_adults=adults,
                num_children=children,
                full_name=full_name,
                email=email,
                phone=phone,
                # username=request.user or None
            )

            # if request.user.is_authenticated:
            #     booking.user=request.user
            #     booking.save()
            # else:
            #     booking.user == None
            #     booking.save()

            for h_id, item in request.session['selection_data_obj'].items():
                room_id = int(item["room_id"])
                room=Room.objects.get(id=room_id)
                booking.room.add(room)

                room_count +=1
                days = total_days
                price = room_type.price
               
                room_price = price*room_count
                total = room_price*days


            booking.payable += float(total)
            booking.before_discount += float(total)
            booking.save()

            return redirect("hotel:checkout", booking.bookingid)

           
            

        hotel = None    
        for h_id, item in request.session['selection_data_obj'].items():
            id = int(item['hotel_id'])
            checkin = item['checkin']
            checkout = item['checkout']
            adults = int(item['adults'])
            children = int(item['children'])
            room_type_ = int(item['room_type'])
            room_id = int(item['room_id'])

            room_type = RoomType.objects.get(id=room_type_)

            date_format = "%Y-%m-%d"
            checkin_date = datetime.strptime(checkin, date_format)
            checkout_date = datetime.strptime(checkout, date_format)

            time_difference = checkout_date - checkin_date
            total_days = time_difference.days

            room_count +=1
            days = total_days
            price = room_type.price

            room_price = price*room_count
            total = room_price*days

            hotel = Hotel.objects.get(id=id)
           



        #     print(h_id, id, checkin, "checkout date is===",checkout, "adults are===",adults, "children are==",children, "room type is==",room_type_, "room id is ===",room_id, room_type) 
        #     print("this should be the formted checkin date ==", checkin_date ,"this is the out date==", checkout_date)
            
        #     print("number of days are ====", total_days,"days" , "rooms checked are==", room_count ,"and the price is==", price, "and it will cost====",room_price,"and the total amount is ====", total)
        
        # print("hotel is =====", hotel)
        context ={
            "data":request.session['selection_data_obj'],
            "total_selected_items": len(request.session['selection_data_obj']),
            "total":total,
            "total_days":total_days,
            "adults":adults,
            "children":children,
            "checkin":checkin,
            "checkout":checkout,
            "hotel":hotel,
        }
        return render(request,"hotel/selected_rooms.html", context)    
    else:
        messages.warning(request, "No room selected")
        return redirect("/")
    
def checkout(request, booking_id):
    booking = Booking.objects.get(bookingid=booking_id)
    if request.method =="POST":
        code = request.POST.get("code")
        # print("todays coupon shoild be======", code)
        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            # print("coupon is ===",code, " already exist and it is ", coupon)
            if coupon in booking.coupons.all():
                print("Coupon ", coupon, "is already activated")
                # messages.warning(request, "Coupon already active")
                return redirect("hotel:checkout", booking.bookingid)

            else:
                if coupon.type=="Percentage":
                    discount = booking.payable * coupon.discount / 100
                else:
                    discount = coupon.discount

                booking.coupons.add(coupon)
                booking.payable -=discount
                booking.saved += discount
                booking.save()


                print("Coupon activated")
                # messages.success(request, "Coupon activated")
                return redirect("hotel:checkout", booking.bookingid)
        except:
            print("coupon does not exist")
            # messages.error(request, "Coupon does not exist")
            return redirect("hotel:checkout", booking.bookingid)

    context ={
        "booking":booking,

    }

    return render(request, "hotel/checkout.html", context)


#     if 'whishlist' in request.session:
#         for h_id, item in request.session['whishlist'].items():
#             print(item)
#             # id = int(item['hotel_id'])
#             # checkin = item['checkin']
#             # checkout = item['checkout']
#             # adults = item['adults']
#             # children = item['children']
#             # room_type_ = int(item['room_type'])
#             # room_id = int(item['room_id'])

#             # room_type = RoomType.objects.get(id=room_type_)

#             # date_format = "%Y-%m-%d"
#             # checkin_date = datetime.strptime(checkin, date_format)
#             # checkout_date = datetime.strptime(checkout, date_format)

            
#             # print("new========", checkout_date - checkin_date)

#             # print("this should be the no of children =====", checkin)
#             # print("this should be the no of children =====", checkout)
#         # print("this should be the checkin id =====", id,  item)
#         # print("this should be the checkin date =====", checkin,  item)
#         # print("this should be the checkout date =====", checkout,  item)
    
#     else:
#         messages.warning(request, "No room selected ")
#         return redirect("/")
#     return render(request, "hotel/selected_rooms.html")


# # def selected_rooms(request):

    total = 0
    room_count = 0
    total_days = 0
    adults = 0
    children = 0
    checkin =""
    checkout =""

    if 'selection_data_obj' in request.session:
        hotel = None
        for h_id, item in request.session['selection_data_obj'].items():
            id = int(item['hotel_id'])
            checkin = item['checkin']
            checkout = item['checkout']
            adults = item['adults']
            children = item['children']
            room_type_ = item['room_type']
            room_id = int(item['room_id'])


            room_type = RoomType.objects.get(id=room_type_)

            # date_format = "%Y-%m-%d"
            # checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
            # checkin_date = datetime.strptime(checkin, date_format)
            # checkout_date = datetime.strptime(checkout, "%Y-%m-%d")

            # time_difference = checkout_date - checkin_date
            # total_days = time_difference.days

            # room_count +=1
            # days = total_days
            # price = room_type.price

            # room_price = price*room_count
            # total = room_price*days

            # hotel = Hotel.objects.get(id=id)

            print("checkin date for today7 is =====", checkin)
            print("checkout  for today7 is date is =====", checkout)


            print("total days ========", total_days)
            # if checkin:
            #     try:
            #         checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
            #         print("checkin date:", checkin_date)

            #     except ValueError as e:
            #         print("Error:", e)

            # else:
            #     print("Error: The checkin date is empty.")

         

            # checkin_date = datetime.strptime(checkin, "%Y %m %d")

            # print("checkin date========", checkin_date)
        context = {
            "data":request.session['selection_data_obj'],
            "total_selected_items": len(request.session['selection_data_obj']),
            "total":total,
            "total_days":total_days,
            "adults":adults,
            "children":children,
            "checkin":checkin,
            "checkout":checkout,
            "hotel":hotel,

        }
                
        return render(request, "hotel/selected_rooms.html" ) 

    else:
        messages.warning(request, "No room selected")
        return redirect("/")

    return render(request, "hotel/selected_rooms.html" )