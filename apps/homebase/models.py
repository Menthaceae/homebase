from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Manager, Owner, Tenant

classification_choices = (
    ("rental", "Rental"),
    ("owned", "Owned")
)

status_choices = (
    ("available", "Available"),
    ("occupied", "Occupied"),
    ("maintenance", "Maintenance")
)

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
    classification = models.CharField(choices=classification_choices, blank=False)
    status = models.CharField(choices=status_choices, blank=False)

class OwnedProperty(models.Model):    
    id = models.AutoField(primary_key=True)
    subproperty = models.OneToOneField(SubProperty, on_delete=models.CASCADE)
    owners = models.ManyToManyField(Owner) 
    start_date = models.DateField(auto_now_add=True)

# Think of it like a rental agreement
class Rental(models.Model):
    id = models.AutoField(primary_key=True)
    subproperty = models.ForeignKey(SubProperty, on_delete=models.CASCADE)    
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    rent = models.FloatField()
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True)