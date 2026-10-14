from django.urls import path
from . import views


urlpatterns = [
  path('<int:homebase_id>/', views.home, name='homebaseHome'),    # Use id in path so users can share links.
  path('create/', views.create, name='create'),
  path('manage/<int:homebase_id>/', views.manage_homebase, name='manage_homebase'),
  path('join/<int:homebase_id>/<int:code>/', views.join, name='join'),
  path('', views.hombaseHome, name='hombaseHome'),
  path('join/', views.join_page, name='join_page'),
  path('dashboard/<int:homebase_id>', views.dashboard, name='dashboard'),
  path('ownerdashboard/', views.owner_dashboard, name='owner_dashboard'),
]