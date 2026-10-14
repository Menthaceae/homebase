from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.homebase.models import Homebase

class Event(models.Model):
    post_to_choices = (
        ("public", "Public"),
        ("homebase", "Homebase"),
        ("nearby", "Nearby"),
    )

    id = models.AutoField(primary_key=True)
    homebase = models.ForeignKey(Homebase, null=True, blank=True, on_delete=models.CASCADE) # Only set if post to homebase
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField()

    start_date = models.DateField(default=timezone.localdate)
    start_time = models.TimeField(auto_now=timezone.localtime)


    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    location = models.CharField()
    body = models.TextField()
    image = models.CharField(blank=True)
    post_to = models.CharField(choices=post_to_choices) 
