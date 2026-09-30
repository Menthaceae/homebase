from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages

# Login authentication logic
# POST auth/login/
# Input user login fields (from apps/public/templates/login.html)
# Returns homepage on valid login credentials, "bad login" on failure 
def login_button(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse("Bad login")

# Register logic
# POST auth/register/
# Input user registration fields (from apps/public/templates/register.html)
# Returns homepage on registration success, "bad registration" on failure
def register_button (request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    return HttpResponse("Bad registration")        
