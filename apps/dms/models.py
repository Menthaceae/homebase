from django.db import models

from django.contrib.auth.models import User

class Message_Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    members = models.ManyToManyField(
        User, 
        related_name='message_groups',
        blank=True
    )

    def __str__(self):
        return self.name or f"Group Chat"


class Message(models.Model):
    id = models.AutoField(primary_key=True)

    message_group = models.ForeignKey(
        Message_Group, 
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    body = models.TextField()

    image = models.ImageField(
        null=True, 
        blank=True, 
        upload_to='messages'
    )

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.author}: {self.body[:40]}"

