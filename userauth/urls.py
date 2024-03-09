from django.urls import path,include
from . import views
app_name = "userauth"

urlpatterns = [
    # path('', include('hotel.urls')),
    path('user_login/', views.user_login, name='user_login' ),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('manager_signup/', views.RegisterView, name='manager_signup'),
    path('manager_login/', views.manager_login, name='manager_login'),
    path('signout/', views.logoutView, name='signout'),
]