from django.urls import path
from . import views
app_name = "userauth"

urlpatterns = [
    path('signup/', views.RegisterView, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutView, name='log out'),
]