from django.urls import path
from user_dashboard import views
from django.contrib.auth import views as auth_view



app_name = "user_dashboard"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('booking-details/<bookingid>', views.booking_details, name='booking_details'),
    path('bookings', views.bookings, name='bookings'),
    path('notifications', views.notifications, name='notifications'),
    path('notification_seen/<id>', views.notification_seen, name='notification_seen'),
    path('wallet', views.wallet, name='wallet'),
    path('profile', views.profile, name='profile'),
    path('add-hotel/', views.add_hotel, name='add_hotel'),
    path('edit-hotel/', views.edit_hotel, name='edit_hotel'),
    
    # food base urls
    path('order_confirmation', views.order_confirmation, name='order_confirmation'),
    path('kitchenBar', views.home, name='home'),
    path('order', views.Order, name='order'),
    path('orderpaid', views.orderpaid, name='orderpaid'),
    
   

#    password change 
    path("change-password/", auth_view.PasswordChangeView.as_view(template_name="user_dashboard/password-reset/change-password.html", success_url="/dashboard/password-changed/"), name="change_password"),
    path("password-changed/", views.password_changed, name="password_changed")
]