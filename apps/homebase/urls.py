from django.urls import path
from . import views


urlpatterns = [
  path('<int:homebase_id>/', views.home, name='homebaseHome'),
  path('create/', views.create, name='create'),
  path('join/<int:homebase_id>/<int:code>/', views.join, name='join'),
  path('', views.hombaseHome, name='hombaseHome'),
  path('dashboard/', views.dashboard, name='dashboard'),
]