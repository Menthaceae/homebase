from django import forms
from django.forms import ModelForm
from .models import Post

class PostCreationForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'body',
            'image',
            'post_to',
            'homebase',
            'likes',
            ]
