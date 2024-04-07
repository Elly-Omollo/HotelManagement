from django import forms
from django.forms import FileInput
from hotel.models import  Hotel, Room, RoomType

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

        widgets = {
            'hotel_id': forms.HiddenInput(),  # Set hotel_id field as a hidden input
            'full_name': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            "image": FileInput(attrs={"onchange": "loadFile(event)", "class":"upload"}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.HiddenInput(attrs={'class': 'form-control'}),
            
        }

class AddHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'

class AddRoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = '__all__'

class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'