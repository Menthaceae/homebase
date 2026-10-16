from django.db import models
from django.contrib.auth.models import User

from apps.homebase.models import Homebase

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    category_choices = (
        ("homebase", "Homebase"),
        ("announcement", "Announcement"),
        ("maintenance", "Maintenance"),
        ("marketplace", "Marketplace"),
        ("event", "Event"),
        ("general", "General"),
    )

    post_to_choices = (
        ("public", "Public"),
        ("homebase", "Homebase")
    )

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField()
    body = models.TextField()
    category = models.CharField(choices=category_choices, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to='posts')    # /static/images/
    post_to = models.CharField(choices=post_to_choices) 
    homebase = models.ForeignKey(Homebase, null=True, blank=True, on_delete=models.CASCADE) # Only set if post to homebase
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0, blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, blank=True)
    likes = models.IntegerField(default=0, blank=True)

    