from django.db import models
from django.contrib.auth.models import User

class PropertyManager(models.Model):
    user_id = models.IntegerField(primary_key=True)

class Homebase(models.Model):
    id = models.AutoField(primary_key=True)
    managed_by = models.OneToOneField(PropertyManager, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    bio = models.TextField(blank=True)
    street_address = models.CharField()
    city = models.CharField()
    state = models.CharField()
    zipcode = models.CharField()
    country = models.CharField()
    name = models.CharField()
    banner = models.CharField()

class SubProperty(models.Model):
    id = models.AutoField(primary_key=True)
    managed_by = models.ManyToManyField(User)
    homebase_id = models.ForeignKey(Homebase, on_delete=models.CASCADE)
    number = models.IntegerField()
    rent = models.FloatField()    

class OwnedProperty(models.Model):    
    id = models.AutoField(primary_key=True)
    subproperty_id = models.OneToOneField(SubProperty, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField()

class PropertyOwner(models.Model):
    user_id = models.IntegerField(primary_key=True) 
    owns = models.ManyToManyField(OwnedProperty)  

class Rental(models.Model):
    id = models.AutoField(primary_key=True)
    subproperty_id = models.ForeignKey(SubProperty, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField()

class Tenant(models.Model):
    user_id = models.IntegerField(primary_key=True)
    rents = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True)         


  
