from django.db import models

class Homebase(models.Model):
    id = models.BigAutoField(primary_key=True)
    street_address = models.CharField()
    city = models.CharField()
    state = models.CharField()
    zipcode = models.CharField()
    country = models.CharField()
    bio = models.TextField(blank=True)