from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse

from apps.posts import views as Posts
from apps.users.models import *
from apps.public.views import *
from .models import *
from .forms import *


"""
Begin Homebase authentication logic and stuff
"""


def code_is_valid(code):
    if (code == code):
        return True


def in_homebase(user, homebase):
    return homebase.users.contains(user)


def manages(user, homebase):
    return homebase.managers.contains(user)


def owns(user, owned_property):
    return owned_property.users.contains(user)


def rents(user, rental):
    return rental.users.contains(user)


"""
End Homebase authentication logic and stuff
"""


# GET homebase/<id>/
def home(request, homebase_id):
    homebase = Homebase.objects.get(id=homebase_id)
    authorized = in_homebase(request.user, homebase)
    if (authorized):
        homebase_posts = Posts.get_homebase_posts(homebase_id)
        context = {
            "homebase_posts": homebase_posts,
            "homebase": homebase
        }
        return render(request, 'homebase.html', context)
    else:
        return HttpResponse("Not authorzied")


# Eventually I will make a thing where it will go to your default Homebase or something
def hombaseHome(request):
    posts = Posts.get_homebase_posts(homebase_id=2)
    context = {
        "posts": posts
    }
    return render(request, 'homebase.html', context)


def manage_homebase(request, homebase_id):
    homebase = Homebase.objects.get(id=homebase_id)
    subproperties_count = homebase.subproperty_set.all().count()
    rented_subproperties_count = Rental.objects.filter(subproperty__homebase=homebase, occupied=True).count()
    owned_subproperties_count = OwnedProperty.objects.filter(subproperty__homebase=homebase).count()
    rented_subproperties = Rental.objects.filter(subproperty__homebase=homebase, occupied=True)
    owned_subproperties = OwnedProperty.objects.filter(subproperty__homebase=homebase)

    if request.method == 'POST':
        sub_form = SubPropertyCreationForm(request.POST)
        rental_form = RentalCreationForm(request.POST)
        owned_email = request.POST.get('owners_email')
        tenant_email = request.POST.get('tenant')

        with transaction.atomic():
            if sub_form.is_valid():
                subproperty = sub_form.save(commit=False)
                subproperty.homebase = homebase
                subproperty.save()

            if rental_form.is_valid():
                if tenant_email is not None and tenant_email != '':
                    user = invite_user(tenant_email, request)
                    tenant = Tenant.objects.create(tenant=user)
                    rental.tenant = tenant
                rental = rental_form.save(commit=False)
                rental.subproperty = subproperty
                subproperty.managed_by.add(request.user)
                rental.save()

            if owned_email:
                user = invite_user(owned_email, request)
                owner = Owner.objects.create(owner=user)
                owned_property = OwnedProperty.objects.create(subproperty=subproperty)
                owned_property.owners.add(owner)
                subproperty.managed_by.add(user)

            return redirect('manage_homebase', homebase_id=homebase.id)
    else:
        sub_form = SubPropertyCreationForm()
        rental_form = RentalCreationForm()

    context = {
        "sub_form": sub_form,
        "rental_form": rental_form,
        "homebase": homebase,
        "rental_subproperties": rented_subproperties,
        "owned_subproperties": owned_subproperties,
        "subproperties_count": subproperties_count,
        "rented_subproperties_count": rented_subproperties_count,
        "owned_subproperties_count": owned_subproperties_count
    }
    return render(request, 'manage.html', context)


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


# GET homebase/join/
def join_page(request):
    return render(request, 'joinhomebase.html')


# GET homebase/dashboard/<homebase_id>/
def dashboard(request, homebase_id):
    homebase = Homebase.objects.get(id=homebase_id)
    authorized = (in_homebase(request.user, homebase) and manages(request.user, homebase))
    if (authorized):
        return render(request, 'dashboard.html')
    else:
        return HttpResponse("Not authorized")

