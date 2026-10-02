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