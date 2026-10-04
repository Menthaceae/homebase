from django.shortcuts import render
from .models import Homebase
from .forms import HomebaseCreationForm
from django.http import HttpResponse
from django.contrib import messages

# GET homebase/
def home(request):
    return render(request, 'homebase.html')

# POST homebase/create/
# Homebase creation logic
def create(request):
    if request.method == 'POST':
        form = HomebaseCreationForm(request.POST)
        if form.is_valid():
            homebase = form.save()
            homebase.save()
            messages.success(request, "Homebase creation successful")
    else:
        form = HomebaseCreationForm()           

    return render(request, 'testcreatehomebase.html', {"form": form})

# GET homebase/join/<homebase_id>/<code>/
# User gets link from property manager.
# User clicks on link.
# If the user is logged in and the code is valid, then they join the homebase.
def join(request, homebase_id, code):
    if (validate_code(code)):
        user = request.user
        user_profile = user.profile
        homebase = Homebase.objects.get(id=homebase_id)
        user_profile.homebases.add(homebase)
        user_profile.save()
        return home(request)

def validate_code(code):
    if (code == code):
        return True