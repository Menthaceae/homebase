from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='homebase'),
  path('create/', views.create, name='create'),
  path('join/<int:homebase_id>/<int:code>/', views.join, name='join'),
]