from django.shortcuts import render
from .models import Homebase
from django.contrib.auth.models import User
from .forms import HomebaseCreationForm
from django.http import HttpResponse
from django.contrib import messages


# GET homebase/
def home(request, homebase_id):
    homebase = Homebase.objects.get(id=homebase_id)
    if (authorize_user(request.user, homebase)):
        context = {"homebase": homebase}
        return render(request, 'testhomebase.html', context)

def hombaseHome(request):
    return render(request, 'homebase.html')

def authorize_user(user, homebase):
    return True

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
        homebase = Homebase.objects.get(id=homebase_id)
        homebase.users.add(user)
        homebase.save()
        return home(request)

def validate_code(code):
    if (code == code):
        return True