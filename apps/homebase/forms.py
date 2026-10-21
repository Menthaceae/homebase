from django import forms
from django.forms import ModelForm
from .models import Announcement, Homebase, MaintenanceRequest, OwnedProperty, Rental, SubProperty

class HomebaseCreationForm(ModelForm):
    class Meta:
        model = Homebase
        fields = ['name', 'street_address', 'city', 'state', 'zipcode', 'country', 'banner', 'bio']

class SubPropertyCreationForm(ModelForm):
    class Meta:
        model = SubProperty
        fields = ['room_number']

class RentalCreationForm(ModelForm):
    class Meta:
        model = Rental
        fields = ['rent', 'occupied', 'start_date', 'end_date']

class MaintenanceRequestForm(ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['title', 'description', 'priority', 'rental']

class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
