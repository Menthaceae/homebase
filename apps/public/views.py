from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib import messages

# GET /
def home(request):
    return render(request, 'home.html')
# You don't need a render login page view because Django already provides one from auth_views.LoginView.as_view


# GET register/
def register(request):
    return render(request, 'register.html')