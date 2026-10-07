from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from apps.posts import views as Posts
from .models import Homebase
from .forms import HomebaseCreationForm


# GET homebase/<id>/
def home(request, homebase_id):
    homebase = Homebase.objects.get(id=homebase_id)
    if (user_in_homebase(request.user, homebase)):
        homebase_posts = Posts.get_homebase_posts(homebase_id)
        context = {
            "homebase_posts": homebase_posts,
            "homebase": homebase
        }
        return render(request, 'homebase.html', context)


def user_in_homebase(user, homebase):
    return user.homebase_set.contains(homebase)


# POST homebase/create/
def create(request):
    error_message = None
    if request.method == 'POST':
        form = HomebaseCreationForm(request.POST)
        if form.is_valid():
            homebase = form.save()
            homebase.save()
            return redirect('/homebase')
        error_message = form.errors.as_text()
    else:
        form = HomebaseCreationForm()
    context = {
        "form": form,
        "error_message": error_message
    }               
    return render(request, 'createhomebase.html', context)


# GET homebase/join/<homebase_id>/<code>/
def join(request, homebase_id, code):
    if (code_is_valid(code)):
        user = request.user
        homebase = Homebase.objects.get(id=homebase_id)
        homebase.users.add(user)
        homebase.save()
        return home(request, homebase_id)


def code_is_valid(code):
    if (code == code):
        return True


# GET homebase/join/
def join_page(request):
    return render(request, 'joinhomebase.html')


# GET homebase/dashboard/<homebase_id>/
def dashboard(request):
    return render(request, 'dashboard.html')