from django.urls import path
from . import views


urlpatterns = [
  path('<int:homebase_id>/', views.home, name='homebaseHome'),
  path('create/', views.create, name='create'),
  path('join/<int:homebase_id>/<int:code>/', views.join, name='join'),
  path('', views.hombaseHome, name='hombaseHome'),
  path('join/', views.join_page, name='join_page')
]