from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.

def login_page(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("/home")
    else:
        return HttpResponse("Bad login")

"""
def login_page(request, username, password):
    user = authenticate(request, username=username, password=password)

    if user is not None:
        return HttpResponse("Good")
    else:
        return HttpResponse("Bad")
"""        