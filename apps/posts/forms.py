from django import forms
from django.forms import ModelForm
from .models import Post

class PostCreationForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'catagory', 'post_to', 'image']
        fields = ['title', 'body', 'category', 'post_to', 'image']

class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'catagory', 'post_to', 'image']
        fields = ['id', 'title', 'body', 'category', 'post_to', 'image']
