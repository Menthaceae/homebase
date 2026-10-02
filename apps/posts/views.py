from django.shortcuts import render, redirect
from .models import Post
from .forms import PostCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib import messages

# GET posts/
def get_all(request):
    posts = Post.objects.all()
    context = {"all_posts": posts}
    # return context
    return render(request, 'testgetallposts.html', context)

# POST posts/create/
def create(request):
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post creation successful")
            return redirect('/posts/')
    else:
        form = PostCreationForm()           

    return render(request, 'testcreatepost.html', {"form": form})

    