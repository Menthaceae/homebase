from django.db import models

class Homebase(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField()
    street_address = models.CharField()
    city = models.CharField()
    state = models.CharField()
    zipcode = models.CharField()
    country = models.CharField()
    banner = models.CharField()
    bio = models.TextField(blank=True)
    # subproperty relationship