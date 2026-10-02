from django.shortcuts import render
from .models import Post
from .forms import PostCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib import messages

# POST posts/create/
def create(request):
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        author = request.user.id
        if form.is_valid():
            post = form.save()
            post.author = author
            post.save()
            messages.success(request, "Post creation successful")
    else:
        form = PostCreationForm()           

    return render(request, 'create_post.html', {"form": form})

    