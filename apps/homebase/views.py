from django.shortcuts import render
from apps.posts import views as Posts
from .models import Homebase
from django.contrib.auth.models import User
from .forms import HomebaseCreationForm
from django.shortcuts import redirect


# GET homebase/
def home(request, homebase_id):
    homebase = Homebase.objects.get(id=homebase_id)
    homebase_posts = Posts.get_homebase_posts(homebase_id)

    if (authorize_user(request.user, homebase)):
        context = {
            "homebase_posts": homebase_posts,
            "homebase": homebase
        }

        return render(request, 'testhomebase.html', context)

# If user in homebase
def is_user_in_homebase(user, homebase):
    return True        

def hombaseHome(request):
    return render(request, 'homebase.html')

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
    if (validate_code(code)):
        user = request.user
        homebase = Homebase.objects.get(id=homebase_id)
        homebase.users.add(user)
        homebase.save()
        return home(request, homebase_id)

def is_code_valid(code):
    if (code == code):
        return True

# GET homebase/join/
def join_page(request):
    return render(request, 'joinhomebase.html')

# GET homebase/dashboard/
def dashboard(request):
    return render(request, 'dashboard.html')
