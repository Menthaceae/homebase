from django.db import models
from django.contrib.auth.models import User
from apps.homebase.models import Homebase

class Event(models.Model):
    post_to_choices = (
        ("public", "Public"),
        ("homebase", "Homebase")
    )

    id = models.AutoField(primary_key=True)
    homebase = models.ForeignKey(Homebase, null=True, blank=True, on_delete=models.CASCADE) # Only set if post to homebase
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField()
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField()
    details = models.TextField()
    image = models.CharField(blank=True)
    post_to = models.CharField(choices=post_to_choices) 
