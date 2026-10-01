from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='homebase'),
  path('create/', views.create, name='create'),
]