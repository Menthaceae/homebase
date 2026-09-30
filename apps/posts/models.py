from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(blank=False)
    body = models.TextField(blank=False)
    status = models.CharField()
    catagory = models.CharField()
    post_to = models.CharField()
    image = models.CharField()
    created_at = models.DateField(auto_now=True)