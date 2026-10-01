from django.shortcuts import render
from .models import Homebase
from .forms import HomebaseCreationForm
from django.http import HttpResponse

# GET homebase/
def home(request):
    return render(request, 'homebase.html')

# POST homebase/create/
# Homebase creation logic
def create(request):
    if request.method == 'POST':
        form = HomebaseCreationForm(request.POST)
        if form.is_valid():
            form = form.save()
            form.save()
            return HttpResponse("Homebase creation success.")

    else:
        form = HomebaseCreationForm()           

    return render(request, 'create_homebase.html', {"form": form})