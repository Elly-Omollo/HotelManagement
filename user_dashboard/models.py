from django.db import models

# Create your models here.
PAYMENT_STATUS = (
    ("NOT PAID","NOT PAID"),
    ("PAID"," PAID"),
    ("PENDING","PENDING"),
    ("processing","processing"),
    ("failed","failed"),
    ("refunded","refunded"),
    ("CANCELLED","CANCELLED"),
)


class MenuItem(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='menu_images')
    price = models.DecimalField(max_digits=12, decimal_places=2, default= 0.00)
    category = models.ManyToManyField('category', related_name = 'item')

    def __str__(self):
        return self.name
    

class category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add = True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=50, blank=True)
    room_type = models.CharField(max_length=100, blank=True, null=True)
    room_number = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    payment_status = models.CharField(max_length=100,choices=PAYMENT_STATUS, default ="NOT PAID", blank=True, null=True)


    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'