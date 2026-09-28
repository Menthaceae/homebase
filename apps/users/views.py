from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.

def login_button(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        # Send to success page
        return HttpResponse("Good login")
    else:
        # Send to failure page
        return HttpResponse("Bad login")
