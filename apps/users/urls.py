from django.urls import path
from apps.users import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login_button, name="login_button"),
    path('register/', views.register_button, name="registerbutton"),
    path('logout/', LogoutView.as_view(), name='logout'),
]
