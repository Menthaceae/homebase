from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from apps import homebase
from apps.posts import views as Posts
from apps.public.views import invite_user
from apps.users.models import Owner, Tenant
from .models import Homebase, OwnedProperty, Rental, SubProperty
from django.contrib.auth.models import User
from .forms import HomebaseCreationForm, RentalCreationForm, SubPropertyCreationForm
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
    posts = Posts.get_homebase_posts(homebase_id=2)
    context = {
        "posts": posts
    }
    return render(request, 'homebase.html', context)

def manage_homebase(request, homebase_id):
    homebase = Homebase.objects.get(id=homebase_id)
    subproperties_count = SubProperty.objects.filter(homebase=homebase).count()
    rented_subproperties_count = Rental.objects.filter(subproperty__homebase=homebase).count()
    owned_subproperties_count = OwnedProperty.objects.filter(subproperty__homebase=homebase).count()
    rented_subproperties = Rental.objects.filter(subproperty__homebase=homebase)
    owned_subproperties = OwnedProperty.objects.filter(subproperty__homebase=homebase)

    if request.method == 'POST':
        sub_form = SubPropertyCreationForm(request.POST)
        rental_form = RentalCreationForm(request.POST)
        owned_email = request.POST.get('owners_email')
        tenant_email = request.POST.get('tenant')
        classification = request.POST.get('classification')

        with transaction.atomic():
            if sub_form.is_valid():
                subproperty = sub_form.save(commit=False)
                subproperty.homebase = homebase
                subproperty.save()
            if classification == 'rental' and subproperty is not None:
                if rental_form.is_valid():
                    rental = rental_form.save(commit=False)
                    rental.subproperty = subproperty
                    rental.homebase = homebase

                    if tenant_email is not None and tenant_email != '':
                        user = invite_user(tenant_email, request)
                        tenant = Tenant.objects.create(tenant=user)
                        rental.tenant = tenant

                    rental.save()
                    subproperty.managed_by.add(request.user)

                    response = render(request, 'cotton/rentedpropertytable.html', {'rental': rental})
                    response['HX-Reswap'] = 'none'
                    response['HX-Trigger'] = 'closedialog'
                    return response

            if classification == 'owned' and subproperty is not None:
                if owned_email:
                    user = invite_user(owned_email, request)
                    owner = Owner.objects.create(owner=user)
                    owned_property = OwnedProperty.objects.create(subproperty=subproperty)
                    owned_property.owners.add(owner)
                    subproperty.managed_by.add(user)

                    response = render(request, 'cotton/ownedpropertytable.html', {'owned': owned_property})
                    response['HX-Reswap'] = 'none'
                    response['HX-Trigger'] = 'closedialog'
                    return response

            return render(request, 'cotton/subpropertyform.html', {
                "sub_form": sub_form,
                "rental_form": rental_form,
                "homebase": homebase
            })
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
