from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib import messages

# GET /
def home(request):
    return render(request, 'home.html')

# GET register/
def register(request):
    return render(request, 'register.html')