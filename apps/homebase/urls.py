from django.urls import path
from . import views


urlpatterns = [
  path('', views.homebase, name='homebase'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('create/', views.create, name='create'),
]