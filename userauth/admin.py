from django.contrib import admin
from userauth.models import User, Profile

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'username']
    list_display = ['username', 'full_name', 'email', 'phone', 'gender']


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'username']
    list_display = ['image','full_name', 'user', 'verified']



admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)