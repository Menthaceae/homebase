from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    photo = models.CharField()

class Manager(models.Model):
    id = models.AutoField(primary_key=True)
    manager = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) # This is an IS-A relationship

class Owner(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) # This is an IS-A relationship

class Tenant(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) # This is an IS-A relationship   