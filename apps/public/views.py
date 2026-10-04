from django.shortcuts import redirect, render
from django.contrib.auth import login as django_login
from django.contrib import messages
from apps.public.forms import CustomUserCreationForm
from django.contrib.auth.models import User

# Homepage
# GET /
def home(request):
    return render(request, 'home.html')

# Register
# GET and POST register/
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            django_login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form}) 
    
# Login
# GET and POST login/
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
            
    return render(request, 'home.html')