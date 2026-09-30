from django.shortcuts import render
from .models import Post
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

# Create your views here.


# POST posts/create/
# Post creation logic
# Input post creation fields from form
# Returns the post id
def create(request):
    user = request.user
    author = user.id
    title = request.POST['title']
    body = request.POST['body']
    status = request.POST['status']
    catagory = request.POST['catagory']
    post_to = request.POST['post_to']
    image = request.POST['image']

    post = Post(
        author = author,
        title = title,
        body = body,
        status = status,
        catagory = catagory,
        post_to = post_to,
        image = image,
    )

    post.save()
    return HttpResponse("Post creation success. Post ID: " + str(post.id))