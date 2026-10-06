from django.shortcuts import render, redirect
from .models import Post
from .forms import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib import messages

# Get all posts
# GET posts/
def get_all(request):
    posts = Post.objects.all().filter(deleted=False)
    context = {"all_posts": posts}
    return context
    # return render(request, 'testgetallposts.html', context)

def get_homebase_posts(homebase_id): 
    homebase_posts = Post.objects.all().filter(deleted=False, post_to="homebase")
    return homebase_posts

def get_public_posts():  
    public_posts = Post.objects.all().filter(deleted=False, post_to="public")
    return public_posts

# Get one post by id
# GET posts/{id}/
def get(request, id):
    post = Post.objects.get(id=id)
    context = {"post": post}
    return render(request, 'testgetonepost.html', context)

# Create post
# POST posts/create/
def create(request):
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # Don't save yet
            post.author = request.user
            post.save()
            messages.success(request, "Post creation successful")
            return redirect('home')
    else:
        form = PostCreationForm()           

    return render(request, 'testcreatepost.html', {"form": form})

# Update a post
# POST posts/update/
def update(request):
    if request.method == 'POST':
        form = PostUpdateForm(request.POST)
        if form.is_valid():
            post_id = form.id
            post = Post.objects.get(post_id)

            if (post.author == request.user):
                post = form.save()
                post.save()
                messages.success(request, "Post update successful")
                return redirect('/posts/' + post_id + '/')
    else:
        form = PostUpdateForm()           

    return render(request, 'testupdatepost.html', {"form": form})

# Delete a post
# POST posts/delete/
def delete(request):
    post_id = request.id
    post = Post.objects.get(id=post_id)

    if (post.author == request.user):
        post.deleted = True
        post.save()
        return get_all()        