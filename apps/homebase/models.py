from django.db import models
from django.contrib.auth.models import User

class Homebase(models.Model):
    id = models.BigAutoField(primary_key=True)
    bio = models.TextField(blank=True)
    street_address = models.CharField()
    city = models.CharField()
    state = models.CharField()
    zipcode = models.CharField()
    country = models.CharField()
    name = models.CharField()
    banner = models.CharField()
    users = models.ManyToManyField(User)