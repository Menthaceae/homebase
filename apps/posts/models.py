from django.db import models
from django.contrib.auth.models import User
from apps.homebase.models import Homebase

class Post(models.Model):
    #("Key", "Value")
    catagory_choices = (
        ("announcement", "Announcement"),
        ("marketplace", "Marketplace")
    )

    post_to_choices = (
        ("public", "Public"),
        ("homebase", "Homebase")
    )

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    homebase = models.ForeignKey(Homebase, null=True, blank=True, on_delete=models.CASCADE) # Only set if post to homebase
    title = models.CharField()
    body = models.TextField()
    category = models.CharField(choices=catagory_choices, blank=True)
    post_to = models.CharField(choices=post_to_choices) 
    image = models.CharField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, blank=True)
    deleted = models.BooleanField(default=False, blank=True)
    likes = models.IntegerField(default=0, blank=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, blank=True)
    likes = models.IntegerField(default=0, blank=True)