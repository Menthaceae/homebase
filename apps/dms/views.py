from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect

from .models import *
from .forms import *


def add_member(Message_Group, User):
    Message_Group.members.add(User)


def create_message_group(request):
    user = request.user
    if request.method == 'POST':
        form = MessageGroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.members.add(user)
            group.save()
            return redirect('get_all_message_groups')
    else:
        form = MessageGroupCreationForm()
    return render(request, 'create-group.html', {'form': form})


def get_all_message_groups(request):
    user = request.user
    message_groups = user.message_group_set.all()

    context = {
        'groups': message_groups,
    }

    return render(request, 'dms.html', context)
    
    
def get_all_messages(request, message_group_id):
    user = request.user
    group = Message_Group.objects.get(id=message_group_id)
    messages = group.message_set.all()
    members = group.members.all()

    if request.method == 'POST':
        form = MessageCreationForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.message_group = group
            message.author = user
            message.save()
            return redirect('/messages/groups/' +str(message_group_id) + '/')
    else:
        form = MessageCreationForm()
   
    context = {
        'messages': messages,
        'members': members,
        'id': message_group_id,
        'form': form,
    }

    return render(request, 'dm.html', context)


def invite(request, message_group_id):
    user = request.user
    group = Message_Group.objects.get(id=message_group_id)

    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            new_members = form.cleaned_data['members']
            for member in new_members:
                group.members.add(member)
            return redirect('/messages/groups/' +str(message_group_id) + '/')
    else:
        form = InviteForm()

    context = {
        'form': form,
        'id': message_group_id,
    }
    return render(request, 'invite.html', context)