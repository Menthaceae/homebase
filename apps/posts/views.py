from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post, Tag
from .forms import *


# Getters 

def get_all_posts():
    """
    Get all posts
    """
    posts = Post.objects.all().filter()
    return posts

def get_public_posts():
    """
    Get all public posts
    """
    public_posts = Post.objects.all().filter(post_to="public")
    return public_posts

def get_homebase_posts(homebase_id):
    """
    Get all homebase posts
    """
    homebase_posts = Post.objects.all().filter(homebase_id=homebase_id)
    return homebase_posts

def get_by_id(request, id):
    """
    Get post by id
    """
    post = Post.objects.get(id=id)
    return post

# CRUD 

@login_required
def create(request):
    """
    Create post

    endpoint: posts/create/
    """
    form = PostCreationForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            selected_tags = request.POST.getlist('tags')

            if selected_tags:
                post.tags.set(selected_tags)
            else:
                general_tag = Tag.objects.get(slug='general')
                post.tags.add(general_tag)            

            messages.success(request, "Post creation successful")
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request, "Your post could not be created. Please check the form.")
            return render(request, 'public/home.html', {"form": form})

    else:
        return render(request, 'home', {"form": form})

@login_required
def update(request, post_id):
    """
    Update post

    endpoint: update/
    """
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == 'POST':
        form = PostCreationForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid:   
            post = form.save()

            # Update tags
            selected_tags = request.POST.getlist("tags")

            if selected_tags:
                post.tags.set(selected_tags)
            else:
                general_tag = get_object_or_404(
                    Tag,
                    slug="general"
                )
                post.tags.set([general_tag])

                messages.success(request, "Post updated successfully.")
                return redirect('home')
    else:
        form = PostCreationForm(instance=post)

        return render(
            request, "posts/partials/post_edit_modal.html",
            {
                "post": post,
                "form": form,
                "tags": Tag.objects.all(),
            }
        )

@login_required
def delete(request, post_id):
    """
    Delete post
    """
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == "POST":
        post.delete()
        return redirect('home')

    return render(request, 'home')

# Comments / Likes / Share

@login_required
def comment(request):
    """
    Comment on post

    endpoint: posts/comment/
    """
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
