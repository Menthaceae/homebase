from django.urls import path
from . import views


urlpatterns = [
  path('<int:homebase_id>/', views.home, name='homebaseHome'),    # Use id in path so users can share links.
  path('create/', views.create, name='create'),
  path('join/<int:homebase_id>/<int:code>/', views.join, name='join_link'),
  path('join/', views.join_page, name='join_page'),
  path('dashboard/<int:homebase_id>', views.dashboard, name='dashboard'),
]