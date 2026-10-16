from django import forms
from django.forms import ModelForm

from .models import *


class PostCreationForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'image',
            'post_to',
            'homebase',
            'likes',
            ]
class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'id', 
            'title',
            'body', 
            'image',
            ] 

# Parent comment and parent post need to be hidden. I think you should be able to insert the object in the front end in the form.
class CommentCreationForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['parent_post', 'parent_comment', 'body']  

