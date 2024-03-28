from django.urls import path
from hotel import views

app_name = "hotel"

urlpatterns = [
    path('', views.index, name='index'),
    path("detail/<slug>/", views.hotel_details, name='hotel_details'),
    path("detail/<slug:slug>/room-type/<slug:rt_slug>/", views.room_type_details, name='room_type_details'),
    path("selected_rooms/", views.selected_rooms, name='selected_rooms'),
    path("checkout/<booking_id>/", views.checkout, name='checkout'),
    path("update_room_status/", views.update_room_status, name='update_room_status'),


    #payment rout
    path("api/create_checkout_session/<bookingid>", views.create_check_out_session, name='api_create_checkout_session'),
    path("success/<bookingid>/", views.payment_success, name='success'),
    path("failed/<bookingid>/", views.payment_failed, name='failed'),

    

]



