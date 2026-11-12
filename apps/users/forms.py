from django import forms
from django.forms import ModelForm

from .models import *

class UserProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = [
            'photo',
            'bio',
        ]