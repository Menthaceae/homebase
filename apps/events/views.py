from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from apps.events.models import Event

# Getters
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
    events = Event.objects.all().order_by('start_date')

    context = {
        "events": events,
    }
    
    return render(request, 'view_events.html', context)

# CRUD
@login_required
def create_event(request):
    """
    Create a new event
    """

    if request.method == "POST":
        form = EventCreationForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()

            messages.success(request, "Event creation successful")
            return redirect("view_all_events")

    else: render(request, "view_events.html", {"form": form })
