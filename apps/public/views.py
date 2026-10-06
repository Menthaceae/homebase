from django.shortcuts import render
from apps.posts import views as Posts
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as django_login
from django.contrib import messages
from apps.public.forms import CustomUserCreationForm
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    public_posts = Posts.get_public_posts()

    context = {
        "public_posts": public_posts
    }

    return render(request, 'home.html', context)

def layout(request):
    return render(request, 'layout.html')

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
    return render(request, "register.html", {
        "page": "register",
        "form": form
        }) 
    
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
            
    return render(request, 'login.html', {"page": "login"})