from django import forms

from hotel.models import Hotel

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'hotel_id', 
            'full_name',
            'name',
            'description',
            'image',
            'address',
            'mobile',
            'status',
        ]