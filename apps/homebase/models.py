from django.db import models
from django.contrib.auth.models import User

classification_choices = (
    ("rental", "Rental"),
    ("owned", "Owned")
)

status_choices = (
    ("operational", "Operational"),
    ("maintenance", "Maintenance")
)

class Homebase(models.Model):
    id = models.AutoField(primary_key=True)
    managers = models.ManyToManyField(User, related_name='managers')
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
    homebase = models.ForeignKey(Homebase, on_delete=models.CASCADE)
    subproperty = models.OneToOneField(SubProperty, on_delete=models.CASCADE)
    owners = models.ManyToManyField(User) 
    start_date = models.DateField(auto_now_add=True)

# Think of it like a rental agreement
class Rental(models.Model):
    id = models.AutoField(primary_key=True)
    homebase = models.ForeignKey(Homebase, on_delete=models.CASCADE)
    subproperty = models.ForeignKey(SubProperty, related_name='rentals', on_delete=models.CASCADE)    
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    rent = models.FloatField()
    tenant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    occupied = models.BooleanField(default=False, blank=True)
