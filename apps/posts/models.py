from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    #("Key", "Value")
    catagory_choices = {
        ("announcement", "Announcement"),
        ("marketplace", "Marketplace"),
    }

    post_to_choices = {
        ("public", "Public"),
        ("homebase", "Homebase"),
    }

    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(blank=False)
    body = models.TextField(blank=False)
    status = models.CharField()
    catagory = models.CharField(choices=catagory_choices,blank=True)
    post_to = models.CharField(choices=post_to_choices,blank=False) 
    image = models.CharField(blank=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank=True) 