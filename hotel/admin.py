from django.contrib import admin
from hotel.models import Hotel, HotelGallery, Room, RoomType, Booking, Activitylog,StaffOnDuty, Coupon ,Notification

# Register your models here.
class hotelgalleryInline(admin.TabularInline):
    model = HotelGallery


class HotelAdmin(admin.ModelAdmin):
    inlines =[hotelgalleryInline]
    list_display=['thumbnail', 'name', 'full_name', 'status']
    prepopulated_fields = {"slug":["name"] }


class StaffAdmin(admin.ModelAdmin):
    list_display=('name', 'phone', 'email')

class RoomAdmin(admin.ModelAdmin):
    list_display=('room_number','room_type', 'hotel', 'is_available')

class RoomTypeAdmin(admin.ModelAdmin):
    list_display=('room_type', 'hotel')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'date')


admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelGallery)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Booking)
admin.site.register(Room, RoomAdmin)
admin.site.register(Activitylog)
admin.site.register(StaffOnDuty, StaffAdmin)
admin.site.register(Coupon)
admin.site.register(Notification, NotificationAdmin)