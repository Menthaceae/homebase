from django.db import models

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(blank=False)
    body = models.TextField(blank=False)
    status = models.CharField()
    catagory = models.CharField()
    post_to = models.CharField()
    image = models.CharField()
    created_at = models.DateField(auto_now=True)