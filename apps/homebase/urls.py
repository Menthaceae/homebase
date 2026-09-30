from django.urls import path
from . import views


urlpatterns = [
  path('', views.homebase, name='homebase'),
  path('create/', views.create, name='create'),
]