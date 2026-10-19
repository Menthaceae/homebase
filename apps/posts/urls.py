from django.urls import path
from . import views

urlpatterns = [
  path('', views.get_all_posts, name='view_all_posts'),
  path('<int:id>/', views.get_by_id, name='view_post'),
  path('create/', views.create_post, name='create_post'),
  path('<int:post_id>/update/', views.update_post, name="update_post"),
  path('<int:post_id>/delete/', views.delete_post, name="delete_post"),
  path('<int:image_id>/delete/', views.delete_image, name="delete_image"),
]