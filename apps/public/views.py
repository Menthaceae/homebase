from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib import messages



# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            User = form.save()
            login(request, User)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})