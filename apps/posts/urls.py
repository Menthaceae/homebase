from django.urls import path
from . import views

urlpatterns = [
  path('', views.get_all_posts, name='get_all'),
  path('<int:id>/', views.get_by_id, name='get_one'),
  path('delete/', views.delete, name='delete'),
  path('create/', views.create, name='create'),
  path('update/', views.update, name='update'),
]