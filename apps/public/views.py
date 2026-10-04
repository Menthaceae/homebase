from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib import messages

# Create your views here.
def home(request):
    """
    View for the home page.
    
    Renders the home.html template.
    """
    return render(request, 'public/home.html', {
        'page': 'page',
    })

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
    return render(request, 'public/register.html', {
        'page': 'register',
        'form': form,
        })