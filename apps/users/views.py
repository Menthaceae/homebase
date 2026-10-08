from django.db import models
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import * 


def set_manager(user):
    new_manager = Manager(manager=user)
    new_manager.save()

def set_owner(user):
    new_owner = Owner(owner=user)
    new_owner.save()

def set_tenant(user):
    new_tenant = Tentant(tenant=user)
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