from django.contrib import admin
from hotel.models import Hotel, HotelGallery, Room, RoomType, Booking, Activitylog,StaffOnDuty, Coupon

# Register your models here.
class hotelgalleryInline(admin.TabularInline):
    model = HotelGallery


class HotelAdmin(admin.ModelAdmin):
    inlines =[hotelgalleryInline]
    list_display=['thumbnail', 'name', 'full_name', 'status']
    prepopulated_fields = {"slug":["name"] }


class StaffAdmin(admin.ModelAdmin):
    list_display=('name', 'phone', 'email')

admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelGallery)
admin.site.register(RoomType)
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Activitylog)
admin.site.register(StaffOnDuty, StaffAdmin)
admin.site.register(Coupon)