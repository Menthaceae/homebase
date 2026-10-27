from collections import defaultdict
import json

from django.db import transaction
from django.db.models import Q, Count, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse

from apps.posts import views as Posts
from apps.events.models import *
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
    is_in_homebase = homebase.users.contains(user) or homebase.managers.contains(user) or user.rental.users.contains(user)
    return is_in_homebase


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
    isManager = False
    current_user = request.user
    homebase = Homebase.objects.get(id=homebase_id)
    users = homebase.users.all().count()
    posts = Posts.get_homebase_posts(homebase_id)
    managers = homebase.managers.all()
    if current_user in managers:
        isManager = True    
    announcements = Announcement.objects.filter(homebase=homebase).order_by('-created_at')[:5]
    events = Event.objects.filter(homebase=homebase).order_by('start_date')[:5]
    occupied = Rental.objects.filter(subproperty__homebase=homebase, occupied=True).count()
    authorized = True
    if (authorized):
        homebase_posts = Posts.get_homebase_posts(homebase_id)
        context = {
            "homebase_posts": homebase_posts,
            "homebase": homebase,
            "users_count": users,
            "occupied_count": occupied,
            "managers": managers,
            "events": events,
            "announcements": announcements,
            "posts": posts,
            "isManager": isManager
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

@login_required
def manage_homebase(request, homebase_id):
    logged_in_user = request.user
    if not logged_in_user.is_authenticated:
        return redirect('/login')
    homebase = Homebase.objects.get(id=homebase_id)
    if (manages(logged_in_user, homebase))== False:
        return HttpResponse("You do not have permission to manage this homebase.", status=403)
    subproperties = SubProperty.objects.filter(homebase=homebase, rentals__isnull=True)
    rented_subproperties = Rental.objects.filter(subproperty__homebase=homebase)
    owned_subproperties = OwnedProperty.objects.filter(subproperty__homebase=homebase)

    if request.method == 'POST':
        sub_form = SubPropertyCreationForm(request.POST)
        rental_form = RentalCreationForm(request.POST)
        owned_email = request.POST.get('owners_email')
        tenant_email = request.POST.get('tenant_email')
        classification = request.POST.get('classification')
        subproperty_id = request.POST.get('subproperty_id')
        saved_successfully = False
        try:
            if rental_form.is_valid():
                with transaction.atomic():
                    if classification == 'rental' and subproperty_id is None and sub_form.is_valid():
                        subproperty = sub_form.save(commit=False)
                        subproperty.homebase = homebase
                        if SubProperty.objects.filter(homebase=homebase, room_number=subproperty.room_number).exists():
                            response = HttpResponse(status=204)
                            response["HX-Trigger"] = json.dumps({
                                "toast": {"message": f"Subproperty with room number {subproperty.room_number} already exists in this homebase.", "variant": "error"},
                                "closedialog": {}
                            })
                            return response
                        subproperty.save()
                    if subproperty_id is not None and subproperty_id != '':
                        subproperty = SubProperty.objects.get(id=subproperty_id)
                    rental = rental_form.save(commit=False)
                    rental.subproperty = subproperty
                    if tenant_email is not None and tenant_email != '':
                        user = invite_user(tenant_email, request)
                        rental.tenant = user
                    rental.save()
                    subproperty.managed_by.add(request.user)
                    saved_successfully = True

            if classification == 'owned' and sub_form.is_valid():
                if owned_email:
                    with transaction.atomic():
                        user = invite_user(owned_email, request)
                        subproperty = sub_form.save(commit=False)
                        subproperty.homebase = homebase
                        subproperty.save()
                        owned_property = OwnedProperty.objects.create(subproperty=subproperty, classification="residential")
                        owned_property.owners.add(user)
                        subproperty.managed_by.add(user)
                        saved_successfully = True
                    

            if saved_successfully:
                response = HttpResponse(status=204)
                response['HX-Refresh'] = 'true'
                return response
            
            return render(request, 'cotton/subpropertyform.html', {
                "sub_form": sub_form,
                "rental_form": rental_form,
                "homebase": homebase,
            }, status=422)
        except Exception as e:
            response = HttpResponse(status=204)
            response["HX-Trigger"] = json.dumps({
                "toast": {"message": f"Something went wrong: {e}", "variant": "error"},
                "closedialog": {}
            })
            print(f"Error occurred: {e}")
            return response

    sub_form = SubPropertyCreationForm()
    rental_form = RentalCreationForm()

    context = {
        "sub_form": sub_form,
        "rental_form": rental_form,
        "homebase": homebase,
        "rental_subproperties": rented_subproperties,
        "owned_subproperties": owned_subproperties,
        "subproperties": subproperties,
        "total_properties_count": len(subproperties) + len(rented_subproperties) + len(owned_subproperties),
    }
    return render(request, 'manage.html', context)


# POST homebase/create/
@login_required
def create(request):
    user = request.user
    error_message = None
    if request.method == 'POST':
        form = HomebaseCreationForm(request.POST, request.FILES)
        if form.is_valid():
            homebase = form.save()
            homebase.save()
            homebase.managers.add(user)
            return redirect('/homebase/manage/' + str(homebase.id) + '/')
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


def count_all_managed_tenants(user):
    managed_homebases = Homebase.objects.filter(managers=user)
    tenant_count = 0
    for managed_homebase in managed_homebases:
        subproperties = managed_homebase.subproperty_set.all()
        for property in subproperties:
            # rentals = property.rentals.all()
            # tenant_count += rentals.count()
            tenant_count = 1
    return tenant_count


@login_required
def dashboard(request):
    user = request.user
    if Homebase.objects.filter(managers=user).exists():
        return redirect('property-manager/')
    if Rental.objects.filter(tenant=user).exists():
        return redirect('tenant/')


# GET homebase/dashboard/property-manager/
@login_required
def property_manager_dashboard(request):
    user = request.user
    manager_name = user.first_name + " " + user.last_name
    events = Event.objects.filter(homebase__managers=user, start_date__gte=timezone.now()).order_by('start_date')[:5]
    total_rent_revenue = Rental.objects.filter(
    subproperty__homebase__managers=user
    ).aggregate(
        total=Coalesce(Sum("rent"), Value(0.0))
    )["total"]
    maintenance_requests = MaintenanceRequest.objects.filter(rental__subproperty__homebase__managers=user)
    print(f"Maintenance requests for manager {manager_name}: {Rental.objects.filter(subproperty__homebase__managers=user)}")
    subproperties_count = SubProperty.objects.filter(homebase__managers=user).count()
    tenants_count = count_all_managed_tenants(user)
    managed_homebases = Homebase.objects.filter(managers=user).annotate(
        properties_count=Count('subproperty'),
        rental_count=Count('subproperty__rentals', filter=Q(subproperty__rentals__isnull=False)),
    )
    properties_count = managed_homebases.count()
    
    context = {
        "tenants_count": tenants_count,
        "properties_count": properties_count,
        "managed_homebases": managed_homebases,
        "total_rent_revenue": total_rent_revenue,
        "subproperties_count": subproperties_count,
        "manager_name": manager_name,
        "maintenance_requests": maintenance_requests,
        "events": events

    }
    return render(request, 'propertyManagerDb.html', context)


#GET homebase/dashboard/owner/
@login_required
def owner_dashboard(request):
    user = request.user
    owned_properties = OwnedProperty.objects.filter(owners=user)
    properties_count = owned_properties.count()

    rentals = []
    for property in owned_properties:
        rentals.append(property.rental_set)

    context = {
        "properties_count": properties_count,
        "owned_properties": owned_properties,
        "rentals_count": len(rentals),
        "rentals": rentals
    }
    return render(request, 'ownerDb.html', context)


@login_required
def tenant_dashboard(request):
    user = request.user
    rentals = (
    Rental.objects
            .filter(tenant=user)
            .select_related("subproperty__homebase")
            .order_by("subproperty__homebase__name", "subproperty__room_number")
        )
    total_rent = rentals.aggregate(total=Coalesce(Sum("rent"), Value(0.0)))["total"]
    upcoming_events = Event.objects.filter(homebase__subproperty__rentals__tenant=user, start_date__gte=timezone.now()).order_by('start_date')[:5]
    maintenanceticket = MaintenanceRequest.objects.filter(rental__tenant=user)
    mainttenance_form = MaintenanceRequestForm()
    grouped_rentals = defaultdict(list)

    if request.method == 'POST':
        try:
            mainttenance_form = MaintenanceRequestForm(request.POST)
            if mainttenance_form.is_valid():
                maintenance_request = mainttenance_form.save(commit=False)
                maintenance_request.save()
                response = HttpResponse(status=204)
                response['HX-Refresh'] = 'true'
                return response
            else:
                return render(request, 'cotton/maintenanceticketform.html', {
                    "maintenance_form": mainttenance_form,
                    "rentals": rentals
                }, status=422)
        except Exception as e:
            response = HttpResponse(status=204)
            response["HX-Trigger"] = json.dumps({
                "toast": {"message": f"Something went wrong", "variant": "error"},
                "closedialog": {}
            })
            print(f"Error occurred: {e}")
            return response

    for rental in rentals:
        homebase = rental.subproperty.homebase
        if homebase:
            grouped_rentals[homebase].append(rental)
    homebase_groups = [
        {'homebase': hb, 'rentals': r_list}
        for hb, r_list in grouped_rentals.items()
    ]
    
    context = {
        "rentals": rentals,
        "total_rent": total_rent,
        "upcoming_events": upcoming_events,
        "homebase_groups": homebase_groups,
        "maintenance_form": mainttenance_form,
        "maintenancetickets": maintenanceticket
    }
    return render(request, 'tenantdb.html', context)

def create_announcement(request, homebase_id):
    homebase = Homebase.objects.get(id=homebase_id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.homebase = homebase
            announcement.created_by = request.user
            announcement.save()
            response = HttpResponse(status=204)
            response['HX-Refresh'] = 'true'
            return response
        else:
            return render(request, 'cotton/announcementform.html', {
                "form": form,
                "homebase": homebase
            }, status=422)
    else:
        form = AnnouncementForm()
    return render(request, 'cotton/announcementform.html', {
        "form": form,
        "homebase": homebase
    })

def update_ticket_status(request, ticket_id):
    ticket = MaintenanceRequest.objects.get(id=ticket_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Open', 'In Progress', 'Closed']:
            ticket.status = new_status
            ticket.save()
            return redirect('propertyManagerDashboard')
        else:
            return HttpResponse("Invalid status", status=400)
    else:
        return render(request, 'cotton/updateticketstatusform.html', {
            "ticket": ticket
    })


def edit_rental(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    tenant_email = request.POST.get('tenant_email')
    if request.method == 'POST':
        form = RentalCreationForm(request.POST, instance=rental)
        if tenant_email:
            user = invite_user(tenant_email, request)
            if rental.tenant != user:
                rental.tenant = user
                rental.save()
        else:
            rental.tenant = user
        if form.is_valid():
            form.save()
            response = HttpResponse(status=204)
            response['HX-Refresh'] = 'true'
            return response
        else:
            return render(request, 'cotton/rentalform.html', {
                "form": form,
                "rental": rental
            }, status=422)
    else:
        form = RentalCreationForm(instance=rental)
    return render(request, 'cotton/rentalform.html', {
        "form": form,
        "rental": rental
    })

def unassign_rental(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    if request.method == 'POST':
        rental.delete()
        response = HttpResponse(status=204)
        response['HX-Refresh'] = 'true'
        return response
    else:
        return render(request, 'cotton/unassignrentalform.html', {
            "rental": rental
        })
