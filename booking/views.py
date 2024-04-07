from datetime import datetime
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import hotel
from hotel.models import Hotel, HotelGallery, Room, RoomType, Booking, Activitylog,StaffOnDuty

# Create your views here.
def check_room_availability(request):
    if request.method == "POST":
        id = request.POST.get("hotel-id")
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")
        adults = request.POST.get("adults")
        children = request.POST.get("children")
        room_type = request.POST.get("room-type")

        hotel = Hotel.objects.get(id=id)
        room_type = RoomType.objects.get(hotel=hotel, slug=room_type)

        # print("this is the check availability form prints for ", hotel)
        # print("the  id is =======", id)
        # print("checkin date =======", checkin)
        # print("cheeck out date =======", checkout)
        # print("adults =======", adults)
        # print("children are =======", children)
        # print("the  room type is =======", room_type)
        # print("the  hotel name is =======",hotel)
        

        
        url = reverse("hotel:room_type_details", args=[hotel.slug, room_type.slug])
        url_with_params = f"{url}?hotel-id={id}&checkin={checkin}&checkout={checkout}&adults={adults}&children={children}&room_type={room_type}" 

        return HttpResponseRedirect(url_with_params)
    


@csrf_exempt
def add_to_selection(request):
    room_selection = {}

    
# grabbing data to be added to a session
    room_selection[str(request.GET['id'])]={
        'hotel_id': request.GET['hotel_id'],
        'hotel_name': request.GET['hotel_name'],
        'room_name': request.GET['room_name'],
        'room_price': request.GET['room_price'],
        'number_of_beds': request.GET['number_of_beds'],
        'room_number': request.GET['room_number'],
        'room_type': request.GET['room_type'],
        'room_id': request.GET['room_id'],
        'checkout': request.GET['checkout'],
        'checkin': request.GET['checkin'],
        'adults': request.GET['adults'],
        'children': request.GET['children'],
    }
# adding seleected data into a session
    if 'selection_data_obj' in request.session:
        if str(request.GET['id']) in request.session['selection_data_obj']:
            selection_data = request.session['selection_data_obj']
            selection_data[str(request.GET['id'])]['adults']=int(room_selection[str(request.GET['id'])]['adults'])
            selection_data[str(request.GET['id'])]['children']=int(room_selection[str(request.GET['id'])]['children'])
            request.session['selection_data_obj'] = selection_data
        else:
            selection_data = request.session['selection_data_obj']
            selection_data.update(room_selection)
            request.session['selection_data_obj'] = selection_data
    else:
         request.session['selection_data_obj'] = room_selection

    data = {
        "data": request.session['selection_data_obj'],
        "Author": "ELLY OKINYI",
        "total_selected_items": len(request.session['selection_data_obj'])
    }

    return JsonResponse(data)



def delete_selection(request):
    hotel_id = str(request.GET['id'])
    if 'selection_data_obj' in request.session:
        if hotel_id in request.session['selection_data_obj']:
            selection_data = request.session['selection_data_obj']
            del request.session['selection_data_obj'][hotel_id]
            request.session['selection_data_obj'] = selection_data


    total=0
    room_count=0
    total_days=0
    adults=0
    children=0
    checkin=""
    checkout=""

    if 'selection_data_obj' in request.session:
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


    context = render_to_string(
        "hotel/async/selected_rooms.html", 
            {
                "data": request.session['selection_data_obj'], 
                "total_selected_item":len(request.session['selection_data_obj']),
                "total": total,
                "total_days": total_days,
                "adults": adults,
                "children": children,
                "checkin": checkin,
                "checkout": checkout,
                "hotel":hotel,
            }
        )
    
    print("context ========", context)
    return JsonResponse({"data": context, "total_selected_item":len(request.session['selection_data_obj'])})