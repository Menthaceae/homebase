from django.shortcuts import render
from django.urls import reverse
from apps.posts import views as Posts
from django.shortcuts import redirect, render
from django.contrib.auth import login as django_login
from django.contrib import messages
from apps.public.forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


# Landing page
def home(request):
    public_posts = Posts.get_public_posts()
    context = {
        "public_posts": public_posts,
    }
    return render(request, 'public/home.html', context)


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
    context = {
        "page": "register",
        "form": form
    }        
    return render(request, "public/register.html", context) 


def events(request):
    return render(request, '/events/')


def invite_user(email, request):
    user, created = User.objects.get_or_create(
        email=email,
        defaults={'username': email}
    )
    if created:
        user.set_unusable_password()
        user.save()

        # Generate secure one-time tokens
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
    
        # Construct activation URL: /accounts/setup/<uidb64>/<token>/

        # setup_url = request.build_absolute_uri(
        #     reverse('complete_onboarding', kwargs={'uidb64': uid, 'token': token})
        # )
        
        # Send email (e.g. using send_mail)
    return user

