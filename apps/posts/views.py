from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib import messages

from .models import Post
from .forms import *


# Only getters
def get_all_posts():
    posts = Post.objects.all().filter()
    return posts


def get_homebase_posts(homebase_id): 
    homebase_posts = Post.objects.all().filter(homebase_id=homebase_id)
    return homebase_posts


def get_public_posts():  
    public_posts = Post.objects.all().filter(post_to="public")
    return public_posts


def get_by_id(request, id):
    post = Post.objects.get(id=id)
    return post


# POST posts/create/
def create(request):
    form = PostCreationForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, "Post creation successful")
            return redirect(' ')
        else:
            print(form.errors)
            messages.error(request, "Your post could not be created. Please check the form.")
            return render(request, 'public/home.html', {"form": form})#TODO: Perserve and display form errors. 
        #TODO: You can't render post_create.html because it's a cotton component, not a Django template

    else:
        return render(request, 'home', {"form": form})



# POST posts/comment/
def comment(request):
    if request.method == 'POST':
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('home')
    else:
        form = CommentCreationForm()
    return render(request, 'cotton/create-post.html', {'form': form})


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
                return redirect('home')
    else:
        form = PostUpdateForm()           
    return render(request, 'testupdatepost.html', {"form": form})


# POST posts/delete/
# def delete(request):
#     post_id = request.id
#     post = Post.objects.get(id=post_id)

#     if (post.author == request.user):
#         post.save()
#         return get_all_posts()        
