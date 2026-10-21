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
    banner = models.ImageField(blank=True, upload_to='homebase')    # /static/images/
    
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


class MaintenanceRequest(models.Model):
    id = models.AutoField(primary_key=True)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='maintenance_requests')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(choices=(
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("complete", "Complete")
    ), default="pending", max_length=20)
    priority = models.CharField(choices=(
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
    ), default="high", max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    homebase = models.ForeignKey(Homebase, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)