from django.contrib import admin
from userauth.models import Customer, User, Profile

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'username']
    list_display = ['username', 'full_name', 'email', 'phone', 'gender']


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'username']
    list_display = ['image','full_name', 'user', 'verified']

class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['email', 'username']
    list_display = ['email', 'username', 'state', 'phone_no']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Customer, CustomerAdmin)