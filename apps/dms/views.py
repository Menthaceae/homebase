from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from .models import *
from .forms import *

@login_required
def list_all_users(request):
    """
    Return list of all users
    """
    UserList = get_user_model()
    users = UserList.objects.exclude(
        id=request.user.id
    ).values(
        'id',
        'username',
        'first_name',
        'last_name'
    )

    return JsonResponse({
        'users': list(users)
    })

def add_member(Message_Group, User):
    Message_Group.members.add(User)

@login_required
def create_group_chat(request):
    """
    Create group chat with member(s)

    endpoint: chat/create/
    """

    if request.method == 'POST':
        member_ids = request.POST.getlist('members')

        # Validate that at least one participant was selected
        if not member_ids:
            messages.error(
                request,
                "Please select at least one participant.",
                extra_tags="reopen_chat"
            )
            return redirect('view_all_messages')

        # Retrieve selected members, excluding the current user
        members = User.objects.filter(
            id__in=member_ids
        ).exclude(
            id=request.user.id
        )

        form = MessageGroupCreationForm(request.POST)

        if form.is_valid():
            # Combine current user and selected members
            all_members = [request.user] + list(members)

            # Generate default chat name
            chat_name = ", ".join(
                member.first_name or member.username
                for member in all_members
            )

            # Truncate if chat_name exceeds 30 characters
            if len(chat_name) > 30:
                chat_name = chat_name[:27] + "..."

            chat = form.save(commit=False)
            chat.name = chat_name
            chat.save()

            # Add the current user to the group
            chat.members.add(request.user)

            # Add the selected members
            chat.members.add(*all_members)

            return redirect('view_all_messages')

    else:
        form = MessageGroupCreationForm()

    return render(request, 'view_all_messages.html', {'form': form})
<<<<<<< HEAD

=======
>>>>>>> 953adcd (Fix chat not loaading)

def view_all_messages(request):
    """
    Render active chat's messages
    """

    chats = Message_Group.objects.filter(
        members=request.user
    ).order_by('-id')

    chat_id = request.GET.get('chat')

    if chat_id:
        active_chat = chats.filter(id=chat_id).first()
    else:
        active_chat = chats.first()

    context = {
        'chats': chats,
        'active_page': 'messages',
        'active_chat': active_chat,
    }

    return render(request, 'chat_groups.html', context)

def get_all_message_groups(request):
    user = request.user
    message_groups = user.message_group_set.all()

    context = {
        'groups': message_groups,
    }

    return render(request, 'dms.html', context)
    
    
@login_required
def get_all_messages(request, message_group_id):
    """
    Render all messages in a group chat
    """

    user = request.user

    group = get_object_or_404(
        Message_Group,
        id=message_group_id,
        members=user
    )

    if request.method == 'POST':
        form = MessageCreationForm(request.POST, request.FILES)

        if form.is_valid():
            message = form.save(commit=False)
            message.message_group = group
            message.author = user
            message.save()

    else:
        form = MessageCreationForm()

    chat_messages = group.messages.select_related('author').order_by('timestamp', 'id')

    members = group.members.all()

    context = {
        'messages': chat_messages,
        'members': members,
        'active_chat': group,
        'id': message_group_id,
        'form': form,
    }

    return render(request, 'cotton/chat_content.html', context)


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