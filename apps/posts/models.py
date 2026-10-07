from django.db import models
from django.contrib.auth.models import User

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
    title = models.CharField(blank=False)
    body = models.TextField(blank=False)
    catagory = models.CharField(choices=catagory_choices, blank=True)
    post_to = models.CharField(choices=post_to_choices, blank=False) 
    image = models.CharField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, blank=True)
    deleted = models.BooleanField(default=False, null=False)
    likes = models.IntegerField(blank=True, null=True)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    body = models.TextField(blank=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, blank=True)
    likes = models.IntegerField(blank=True, null=True)