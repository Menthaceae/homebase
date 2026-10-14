from django import forms
from django.forms import ModelForm
from .models import Homebase, OwnedProperty, Rental, SubProperty

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
