from django.db import models
from django.contrib.auth.models import User

class Manager(models.Model):
    id = models.AutoField(primary_key=True)
    manager = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) # This is an IS-A relationship

# This is an IS-A relationship
class Owner(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) # This is an IS-A relationship

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
    room_number = models.IntegerField()

class OwnedProperty(models.Model):    
    id = models.AutoField(primary_key=True)
    subproperty = models.OneToOneField(SubProperty, on_delete=models.CASCADE)
    owners = models.ManyToManyField(Owner) 
    start_date = models.DateField(auto_now_add=True)
    status = models.CharField()

# Think of it like a rental agreement
class Rental(models.Model):
    id = models.AutoField(primary_key=True)
    subproperty = models.ForeignKey(SubProperty, on_delete=models.CASCADE)    
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField()
    rent = models.FloatField()

class Tenant(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.OneToOneField(User, on_delete=models.CASCADE) # This is an IS-A relationship
    rental = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True, blank=True)     