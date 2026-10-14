from django.urls import path
from . import views

urlpatterns = [
  path('', views.get_all_posts, name='view_all_posts'),
  path('<int:id>/', views.get_by_id, name='view_post'),
  # path('delete/<int:id>', views.delete, name='delete_post'),
  path('create/', views.create, name='create_post'),
  path('update/', views.update, name='update_post'),
]