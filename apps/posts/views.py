from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

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
def create_post(request):
    """
    Create post
    endpoint: posts/create/
    """

    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES)

        # Debug
        print("MEDIA ROOT:", settings.MEDIA_ROOT)
        print("UPLOADED FILES:", request.FILES)
        print("IMAGE FILES:", request.FILES.getlist("images"))

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Save tags
            selected_tags = request.POST.getlist("tags")

            if selected_tags:
                post.tags.set(selected_tags)
            else:
                general_tag = Tag.objects.get(slug="general")
                post.tags.add(general_tag)

            # Save images
            for image in request.FILES.getlist("images"):
                PostImage.objects.create(
                    post=post,
                    image=image
                )

            print("SAVED IMAGES:", post.images.count())

            messages.success(request, "Post creation successful")
            return redirect("home")

        else:
            print("FORM ERRORS:", form.errors)
            messages.error(
                request,
                "Your post could not be created. Please check the form."
            )

            return render(
                request,
                "public/home.html",
                {
                    "form": form,
                    "tags": Tag.objects.all(),
                }
            )

    else:
        form = PostCreationForm()

    return render(
        request,
        "public/home.html",
        {
            "form": form,
            "tags": Tag.objects.all(),
        }
    )

@login_required
def update_post(request, post_id):
    """
    Update post
    """
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == "POST":
        form = PostUpdateForm(
                    request.POST,
                    request.FILES,
                    instance=post
                )
        
        if form.is_valid():
            post = form.save()

            #Save updated tags
            selected_tags = request.POST.getlist("tags")
            if selected_tags:
                post.tags.set(selected_tags)
            else:
                general_tag = get_object_or_404(Tag, slug="general")
                post.tags.set([general_tag])

            # Save updated images
            for image in request.FILES.getlist("images"):
                PostImage.objects.create(
                    post=post,
                    image=image
                )

            messages.success(request, "Post updated successfully.")
            return redirect('home')
        else:
            print("FORM ERRORS:", form.errors)
            messages.error(request, "Your post could not be updated. Please check the form.")
            return redirect('home')
        
    else:
        form = PostUpdateForm(instance=post)
        return render(request, 'public/home.html', {
            "post": post,
            "form": form,
            "tags": Tag.objects.all()
            })

@login_required
def delete_post(request, post_id):
    """
    Delete post
    """
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    print("POST ID", post_id)
    print("ID", str(post.id))

    post.delete()
    return redirect('home')


def delete_image(request, image_id):
    """
    Delete image
    """
    image = get_object_or_404(
        PostImage,
        id=image_id
    )

    if request.method == "POST":
        image.delete()
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
