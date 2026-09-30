from django.shortcuts import render
from .models import Post
# from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.


# POST posts/create/
# Post creation logic
# Input post creation fields from form
# Returns the post id
def create(request):
    title = request.POST['title']
    body = request.POST['body']
    status = request.POST['status']
    catagory = request.POST['catagory']
    post_to = request.POST['post_to']
    image = request.POST['image']

    post = Post(
        title = title,
        body = body,
        status = status,
        catagory = catagory,
        post_to = post_to,
        image = image,
    )

    post.save()
    return HttpResponse("Post creation success. Post ID: " + str(post.id))