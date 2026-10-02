from django import forms
from django.forms import ModelForm
from .models import Post

class PostCreationForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'catagory', 'post_to', 'image']