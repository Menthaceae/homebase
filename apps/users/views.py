from django.db import models
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.db.models.signals import post_save
from django.dispatch import receiver


from apps.users.forms import UserProfileForm
from apps.posts.models import Post

from .models import * 

def set_manager(user):
    new_manager = Manager(manager=user)
    new_manager.save()

def set_owner(user):
    new_owner = Owner(owner=user)
    new_owner.save()

def set_tenant(user):
    new_tenant = Tenant(tenant=user)
    new_tenant.save()

def remove_manager(user):
    manager = Manager.objects.get(manager=user)
    manager.delete()

def remove_owner(user):
    owner = Owner.objects.get(owner=user)
    owner.delete()

def remove_tenant(user):
    tenant = Tenant.objects.get(tenant=user)
    tenant.delete()

def is_manager(user):
    return hasattr(user, 'manager')
    
def is_owner(user):
    return hasattr(user, 'owner')

def is_tenant(user):
    return hasattr(user, 'tenant')

# Profile views

def get_profile_context(user, form=None):
    """
    Get user profile context
    """
    posts = Post.objects.filter(author=user).order_by('-created_at')
    profile = Profile.objects.get(user=user)

    return {
        'profile': profile,
        'form': form or UserProfileForm(),
        'posts': posts,
        # 'post_count': posts.count(),
    }

@login_required
def profile(request):
    """
    Renders user's profile page
    """

    context = get_profile_context(request.user)

    return render(request, 'users/profile.html', context)

def instantiate_profile(user):
    profile = Profile()
    profile.user = user
    profile.phone_number = 0
    profile.bio = "Edit bio here"
    profile.save()

@login_required
def update_profile(request):
    """
    Update a user's profile details (profile photo or bio)
    """

    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
            )
        
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            context = get_profile_context(request.user, form)
            return render(request, 'profile.html', context)
        
    return redirect('profile')