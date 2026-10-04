from django import forms
from django.forms import ModelForm
from .models import Homebase

class HomebaseCreationForm(ModelForm):
    class Meta:
        model = Homebase
        fields = ['name', 'street_address', 'city', 'state', 'zipcode', 'country', 'banner', 'bio']