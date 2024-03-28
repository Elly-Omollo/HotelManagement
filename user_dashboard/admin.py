from django.contrib import admin
from user_dashboard.models import MenuItem, category, OrderModel

# Register your models here.
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')

admin.site.register(MenuItem)
admin.site.register(category)
admin.site.register(OrderModel)
