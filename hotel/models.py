from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from userauth.models import User
import shortuuid
from taggit.managers import TaggableManager
# Create your models here.
#chosices
HOTEL_STATUS = (
    ("Live","Live"),
    ("Disabled","Disabled"),
    ("in repair","in repair"),
)

ICON_TYPE = (
    ("Bootstrap","Bootstrap"),
    ("Fontawesome","Fontawesome"),
    ("Sanserif","Sanserif"),
)

PAYMENT_STATUS = (
    ("NOT PAID","NOT PAID"),
    ("PAID"," PAID"),
    ("PENDING","PENDING"),
    ("Processing","Processing"),
    ("failed","failed"),
    ("refunded","refunded"),
    ("CANCELLED","CANCELLED"),
)

NOTIFICATION_TYPE = (
    ("Booking Confirmed","Booking Confirmed"),
    ("Booking Cancelled","Booking Cancelled"),
   
)








class Hotel(models.Model):
    full_name = models.ForeignKey(User, on_delete=models.CASCADE)
    name =models.CharField(max_length=100, null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='hotel_gallery')
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=30,null=True, blank=True)
    status = models.CharField(max_length=20,choices=HOTEL_STATUS, default="Live")
    featured = models.BooleanField(default=False)

    facebook = models.URLField(max_length=2000, blank=True, null=True)
    twitter = models.URLField(max_length=2000, blank=True, null=True)
    instagram = models.URLField(max_length=2000, blank=True, null=True)

    tags = TaggableManager(blank=True)
    views = models.IntegerField(default=0)
    hotel_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123")
    slug = models.CharField(max_length=100,null=True, blank=True)
    

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.name)+'-'+str(uniqueid.lower())

        super(Hotel, self).save(*args, **kwargs)

    # @property
    def thumbnail(self):
        return mark_safe(f"<img src='{self.image.url}' width='50', height='50' style='object-fit:cover; border-radius:10px;'/>")
        # return mark_safe("<img src='%s' width='50', height='50' style='object-fit:cover; border-radius:6px;'/>" %(self.image.url))
    
    def hotel_gallery(self):
        return HotelGallery.objects.filter(hotel=self)

    def hotel_room_types(self):
        return RoomType.objects.filter(hotel=self)


class  HotelGallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.FileField(upload_to='hotel_gallery')
    hgid = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123")
    
    def __str__(self):
        return str(self.hotel.name)
    
    class Meta:
        verbose_name_plural = "hotel gallery"

class HotelFeatures(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    icon_type = models.CharField(max_length=100,choices=ICON_TYPE, default="Bootstrap")
    icon = models.CharField(max_length=100, null=True, blank = True)
    name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "hotel features"


class HotelFaqs(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000,)
    answer = models.CharField( max_length= 1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question)
    
    class Meta:
        verbose_name_plural = "FAQs"


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00)
    number_of_beds = models.PositiveIntegerField(default=1)
    room_capsity = models.PositiveIntegerField(default=0)
    roomtypeid = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123")
   

    slug = models.CharField(max_length=100,null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.room_type}"
    
    class Meta:
        verbose_name_plural = "Room Type"

    def room_count(self):
        Room.objects.filter(room_type=self).count()


    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.hotel.name)+'-'+str(uniqueid.lower())

        super(RoomType,self).save(*args, **kwargs)



class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    room_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123")


    def __str__(self):
        return f"{self.room_type.room_type} - {self.hotel.name} "
    
    class Meta:
        verbose_name_plural = "Rooms"

    def price(self):
        return self.room_type.price
    
    def number_of_beds(self):
        return self.room_type.number_of_beds
    
    def hotel_room_type(self):
        return RoomType.objects.filter(hotel=self)
    
    def hotel_gallery(self):
        return HotelGallery.objects.filter(hotel=self)



#booking models
class Booking(models.Model):
    username = models.ForeignKey(User, null= True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=100)

    hotel= models.ForeignKey(Hotel, on_delete=models.PROTECT)
    room_type = models.ForeignKey(RoomType,on_delete=models.PROTECT)
    room = models.ManyToManyField(Room)
    before_discount=models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payable = models.DecimalField(max_digits=12, decimal_places=2,default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2,default=0.00)

    check_in_date = models.DateField()
    check_out_date = models.DateField()

    total_days = models.PositiveIntegerField(default=0)
    number_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)

    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    checked_in_tracker = models.BooleanField(default=False)
    checked_out_tracker = models.BooleanField(default=False)

    payment_status = models.CharField(max_length=100,choices=PAYMENT_STATUS, default ="NOT PAID")
    coupons = models.ManyToManyField("hotel.Coupon", blank=True)
    date = models.DateTimeField(auto_now_add=True)
    success_id = ShortUUIDField(length=6, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123")
 
    bookingid = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123")
   
    def __str__(self):
        return f"{self.bookingid}"
    
    def rooms(self):
        return self.room.all().count()
    
class Activitylog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT)
    guest_out = models.DateTimeField()
    guest_in = models.DateTimeField()
    activity_description = models.TextField(null= True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking.id}"
    
class StaffOnDuty(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT)
    staff_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123")
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True,blank=True)
    phone = models.CharField(max_length=100, null=True,blank=True)
    email = models.EmailField(max_length=1000, null=True, blank=True)
        
class Coupon(models.Model):
    code = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000, default="Percentage")
    discount = models.IntegerField(default=1)
    redemptions = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    active =models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    cid = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmnopqrstuvwxyz123")
    
    def __str__(self):
        return f"{self.code}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.booking.bookingid}"