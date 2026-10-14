from django.forms import ModelForm
from .models import Event

class EventCreationForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'location',
            'body',
            'image',
            'post_to',
        ]