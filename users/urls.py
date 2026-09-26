from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('login/', views.login_button, name="login_button"),
]
