from django.db import models
from django.contrib.auth.models import User
from apps.homebase.models import Homebase

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    homebases = models.ManyToManyField(Homebase, blank=True)
    phone_number = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    photo = models.CharField()