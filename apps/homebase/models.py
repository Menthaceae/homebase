from django.db import models
from django.contrib.auth.models import User

classification_choices = (
    ("rented", "rented"),
    ("residential", "residential"),
)

status_choices = (
    ("operational", "Operational"),
    ("maintenance", "Maintenance")
)

class Homebase(models.Model):
    id = models.AutoField(primary_key=True)
    managers = models.ManyToManyField(User, related_name='managed_homebases')
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
    owners = models.ManyToManyField(User, related_name='owned_properties') 
    start_date = models.DateField(auto_now_add=True)
    classification = models.CharField(choices=classification_choices, default="residential", max_length=20)

# Think of it like a rental agreement
class Rental(models.Model):
    id = models.AutoField(primary_key=True)
    subproperty = models.ForeignKey(SubProperty, related_name='rentals', on_delete=models.CASCADE)    
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    rent = models.FloatField()
    tenant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    occupied = models.BooleanField(default=False, blank=True)
    owned_property = models.ForeignKey(OwnedProperty, on_delete=models.SET_NULL, null=True, blank=True)
