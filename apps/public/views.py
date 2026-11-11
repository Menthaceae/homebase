from logging import exception

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render
from apps.homebase.models import Homebase, Rental, SubProperty
from django.shortcuts import redirect, render
from django.contrib.auth import login as django_login
from django.contrib import messages
from apps.public.forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from apps.posts.models import Tag
from apps.posts.views import get_public_posts, get_homebase_posts
from apps.homebase.views import get_homebase

# Landing page
def home(request):
    if not request.user.is_authenticated:
        return redirect('onboarding/')

    query = request.GET.get('query')
    
    if get_homebase(request.user) is None:
        homebase_id = 0
    else:
        homebase_id = get_homebase(request.user).id

    if query is None:
        public_posts = get_public_posts()
        homebase_posts = get_homebase_posts(homebase_id)
        posts = public_posts | homebase_posts
    else:
        public_posts_search_title = get_public_posts().filter(title__icontains=query)
        public_posts_search_body = get_public_posts().filter(body__icontains=query)
        public_posts = public_posts_search_title | public_posts_search_body
        homebase_posts_search_title = get_homebase_posts(homebase_id).filter(title__icontains=query)
        homebase_posts_search_body = get_homebase_posts(homebase_id).filter(body__icontains=query)
        homebase_posts = homebase_posts_search_title | homebase_posts_search_body
        posts = public_posts | homebase_posts


    tags = Tag.objects.all()
    context = {
        "active_page": "home",
        "posts": posts,
        "tags": tags,
    }
    return render(request, 'public/home.html', context)


def layout(request):
    return render(request, 'layout.html')

# GET and POST register/
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            django_login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    context = {
        "active_page": "register",
        "form": form
    }        

    return render(request, "public/register.html", context) 

def events(request):
    return render(request, '/events/')


def invite_user(email, request):
    user, created = User.objects.get_or_create(
        email=email,
        defaults={'username': email}
    )
    if created:
        user.set_unusable_password()
        user.save()

        # Generate secure one-time tokens
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
    
        # Construct activation URL: /accounts/setup/<uidb64>/<token>/

        # setup_url = request.build_absolute_uri(
        #     reverse('complete_onboarding', kwargs={'uidb64': uid, 'token': token})
        # )
        
        # Send email (e.g. using send_mail)

    return user


def complete_onboarding(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/')
    return render(request, 'onboarding.html')

@require_GET
def check_renter_email(request):

    email = request.GET.get('email', '').strip().lower()
    if not email:
        return JsonResponse({'found': False, 'error': 'Email is required.'}, status=400)

    rental = Rental.objects.filter(tenant__email=email).select_related('subproperty').first()

    if rental:
            return JsonResponse({
                'found': True,
                'homebase_name': rental.subproperty.homebase.name,
                'unit_number': rental.subproperty.room_number if rental.subproperty else 'Unassigned',
                'tenant': {
                    'first_name': rental.tenant.first_name,
                    'last_name': rental.tenant.last_name,
                    'username': rental.tenant.username,
                }
            })

    return JsonResponse({
        'found': False,
        'error': 'No pending lease found for this email. Contact your property manager.'
    }, status=404)


@require_POST
@transaction.atomic
def onboarding_manager_submit(request):
    try:
        post = request.POST
        
        # 1. Validate Passwords
        pwd1 = post.get('password1')
        pwd2 = post.get('password2')
        if pwd1 != pwd2:
            response = JsonResponse({'error': "Passwords do not match."})
            response.status_code = 400
            return response

        # 2. Create Manager User
        user = User.objects.create_user(
            username=post.get('username'),
            email=post.get('email'),
            first_name=post.get('first_name'),
            last_name=post.get('last_name'),
            password=pwd1
        )

        # 3. Create Homebase Complex
        homebase = Homebase.objects.create(
            name=post.get('name'),
            banner=request.FILES.get('banner'),
            bio=post.get('bio'),
            street_address=post.get('street_address'),
            city=post.get('city'),
            state=post.get('state'),
            zipcode=post.get('zipcode'),
            country=post.get('country'),
        )
        homebase.managers.add(user)

        # 4. Batch Create Sub-Properties
        num_units = int(post.get('num_units', 10))
        start_unit = int(post.get('start_unit_num', 101))
        
        sub_properties = [
            SubProperty(
                homebase=homebase,
                room_number=str(start_unit + i),
            )
            for i in range(num_units)
        ]
        SubProperty.objects.bulk_create(sub_properties)

        django_login(request, user)
        return redirect('/homebase/dashboard/property-manager/') 
    except Exception as e:
        return JsonResponse({
            "error": str(e).split("DETAIL:")[-1].strip()
        }, status=400)


@require_POST
@transaction.atomic
def onboarding_renter_submit(request):
    try:
        post = request.POST
        email = post.get('email', '').strip().lower()

        pwd1 = post.get('password1')
        pwd2 = post.get('password2')
        if pwd1 != pwd2:
            response = JsonResponse({'error': "Passwords do not match."})
            response.status_code = 400
            return response

        user = User.objects.get(email=email)

        # Create Renter User
        user.set_password(pwd1)
        user.first_name = post.get('first_name')
        user.last_name = post.get('last_name')
        user.save()

        django_login(request, user)
        return redirect('/homebase')
    except Exception as e:
        return JsonResponse({
            "error": str(e).split("DETAIL:")[-1].strip()
        }, status=400)
