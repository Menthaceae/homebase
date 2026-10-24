from django.db import models

from django.contrib.auth.models import User

class Message_Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    members = models.ManyToManyField(User, null=True, blank=True)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    message_group = models.ForeignKey(Message_Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    body = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='messages')
    timestamp = models.DateTimeField(auto_now=True)

