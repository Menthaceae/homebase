from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Manager, Owner, Tenant

class Homebase(models.Model):
    id = models.AutoField(primary_key=True)
    managers = models.ManyToManyField(Manager)
    users = models.ManyToManyField(User)
    bio = models.TextField(blank=True)
    street_address = models.CharField()
    city = models.CharField()
    state = models.CharField()
    zipcode = models.CharField()
    country = models.CharField()
    name = models.CharField()
    banner = models.CharField(blank=True)
    
class SubProperty(models.Model):
    id = models.AutoField(primary_key=True)
    managed_by = models.ManyToManyField(User)
    homebase = models.ForeignKey(Homebase, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)

class OwnedProperty(models.Model):    
    id = models.AutoField(primary_key=True)
    classification = models.CharField()
    subproperty = models.OneToOneField(SubProperty, on_delete=models.CASCADE)
    owners = models.ManyToManyField(Owner) 
    start_date = models.DateField(auto_now_add=True)
    status = models.CharField()

# Think of it like a rental agreement
class Rental(models.Model):
    id = models.AutoField(primary_key=True)
    subproperty = models.ForeignKey(SubProperty, on_delete=models.CASCADE)  
    owned_property = models.ForeignKey(OwnedProperty, on_delete=models.CASCADE, null=True, blank=True) 
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField()
    rent = models.FloatField()
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True)
    occupied = models.BooleanField(default=False, blank=True)