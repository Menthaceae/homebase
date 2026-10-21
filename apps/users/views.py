from django.db import models
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


from .models import * 


def set_manager(user):
    new_manager = Manager(manager=user)
    new_manager.save()

def set_owner(user):
    new_owner = Owner(owner=user)
    new_owner.save()

def set_tenant(user):
    new_tenant = Tenant(tenant=user)
    new_tenant.save()

def remove_manager(user):
    manager = Manager.objects.get(manager=user)
    manager.delete()

def remove_owner(user):
    owner = Owner.objects.get(owner=user)
    owner.delete()

def remove_tenant(user):
    tenant = Tenant.objects.get(tenant=user)
    tenant.delete()

def is_manager(user):
    return hasattr(user, 'manager')
    
def is_owner(user):
    return hasattr(user, 'owner')

def is_tenant(user):
    return hasattr(user, 'tenant')

def profile(request):
    """
    Renders user's profile page
    """

    return render(request, 'users/profile.html')