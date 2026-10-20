from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="public/login.html", extra_context={"page": "login"}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('onboarding/', views.complete_onboarding, name='complete_onboarding'),
    path('api/check-renter/', views.check_renter_email, name='api_check_renter'),
    path('onboarding/manager/submit/', views.onboarding_manager_submit, name='onboarding_manager_submit'),
    path('onboarding/renter/submit/', views.onboarding_renter_submit, name='onboarding_renter_submit'),
]