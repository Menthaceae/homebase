from django.shortcuts import render, redirect, get_object_or_404

from apps.homebase.models import Homebase, Rental
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from apps.events.models import Event
from apps.posts.models import Tag

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
    tags = Tag.objects.all()

    context = {
        "events": events,
        "tags": tags,
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
        homebase_id = request.POST.get('homebase')
        user = request.user
        if homebase_id:
            homebase = get_object_or_404(Homebase, id=homebase_id)
            form.instance.homebase = homebase
        else:
            if Homebase.objects.filter(managers=user).exists() and form.instance.post_to != "public":
                form.instance.homebase = Homebase.objects.filter(managers=user).first()
            else:
                rentals = Rental.objects.filter(tenant=user)
                if rentals.exists():
                        form.instance.homebase = rentals.first().subproperty.homebase
                else:
                        form.instance.homebase = None

        if form.is_valid():
            event = form.save(commit=False)
            event.author = user
            event.save()

            messages.success(request, "Event creation successful")
            if request.POST.get('homebase'):
                return redirect(f"/homebase/{request.POST.get('homebase')}#events")
            else:
                return redirect("view_all_events")
        else:
            return render(request, "view_events.html", {"form": form})

    else: render(request, "view_events.html", {"form": form })

@login_required
def update_event(request, event_id):
    event = get_object_or_404(
        Event,
        id=event_id,
        author=request.user
    )

    if request.method == "POST":
        form = EventUpdateForm(
            request.POST,
            request.FILES,
            instance=event
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
        else:
            print("FORM ERRORS:", form.errors)
            messages.error(
                request,
                "Your event could not be updated. Please check the form."
            )

    return redirect('view_all_events')