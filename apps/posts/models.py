from django.db import models

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.charField(empty=False)
    body = models.TextField(empty=False)
    status = models.charField()
    catagory = models.charField()
    postTo = models.charField()
    image = models.charField()
    created_at = models.DateField(auto_now=True)