from django.urls import path
from hotel import views

app_name = "hotel"

urlpatterns = [
    path('', views.index, name='index'),
    path("detail/<slug>/", views.hotel_details, name='hotel_details'),
    path("detail/<slug:slug>/room-type/<slug:rt_slug>/", views.room_type_details, name='room_type_details'),
    path("selected_rooms/", views.selected_rooms, name='selected_rooms'),
    path("checkout/<booking_id>/", views.checkout, name='checkout'),
    

]



