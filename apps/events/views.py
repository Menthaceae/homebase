from django.shortcuts import render, redirect
from .models import Event
from .forms import *
from django.contrib import messages

# Create your views here.

def get_all_events(request):
    """
    Returns all events ordered by start date
    """
    events = Event.objects.all().order_by('start_date')
    
    return render(request, 'events/view_events.html', {
        'events': events
    })

def view_all(request):
    """
    Returns view all events page
    """
    return render(request, 'view_events.html')

