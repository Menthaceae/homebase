from django.db import models
from django.contrib.auth.models import User

class Homebase(models.Model):
    id = models.AutoField(primary_key=True)
    bio = models.TextField(blank=True)
    street_address = models.CharField()
    city = models.CharField()
    state = models.CharField()
    zipcode = models.CharField()
    country = models.CharField()
    name = models.CharField()
    banner = models.CharField()
    users = models.ManyToManyField(User)

class SubProperty(models.Model):
    id = models.AutoField(primary_key=True)
    managed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    homebase_id = models.ForeignKey(Homebase, on_delete=models.CASCADE)
    number = models.IntegerField()
    rent = models.FloatField()    

class PropertyManager(models.Model):
    user_id = models.IntegerField(primary_key=True)
    # Managed properties on properties side

class PropertyOwner(models.Model):
    user_id = models.IntegerField(primary_key=True)
    # Owned properties on properties side    

class OwnedProperty(models.Model):    
    id = models.AutoField(primary_key=True)
    owner_id = models.OneToOneField(PropertyOwner, on_delete=models.SET_NULL, null=True) # Don't remove property if the owner is deleted
    subproperty_id = models.OneToOneField(SubProperty, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField()

class Rental(models.Model):
    id = models.AutoField(primary_key=True)
    # tenant_id relation on tenant side
    subproperty_id = models.OneToOneField(SubProperty, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField()

class Tenant(models.Model):
    user_id = models.IntegerField(primary_key=True)
    rentals = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True)      

  