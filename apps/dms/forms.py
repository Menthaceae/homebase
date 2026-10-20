from django import forms
from django.forms import ModelForm

from .models import *


class MessageGroupCreationForm(ModelForm):
    class Meta:
        model = Message_Group
        fields = [
            'name',
            'members'
        ]

class MessageCreationForm(ModelForm):
    class Meta:
        model = Message
        fields = [
            'body',
            'image',
        ]

class InviteForm(ModelForm):
    class Meta:
        model = Message_Group
        fields = [
            'members', 
        ]