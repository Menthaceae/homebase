from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
from .models import Homebase
from django.http import HttpResponse

def homebase(request):
    return render(request, 'homebase.html')

def dashboard(request):
    return render(request, 'dashboard.html')

# GET homebase/create/
# Renders homebase creation page

# POST homebase/create/
# Homebase creation logic
# Input homebase creation fields from form
# Returns the homebase id 
def create(request):
    street_address = request.POST['street_address']
    city = request.POST['city']
    state = request.POST['state']
    zipcode = request.POST['zipcode']
    country = request.POST['country']
    bio = request.POST['bio']

    homebase = Homebase(
                street_address = street_address,
                city = city,
                state = state,
                zipcode = zipcode,
                country = country,
                bio = bio)

    homebase.save()
    return HttpResponse("Homebase creation success. Homebase ID: " + str(homebase.id))       
