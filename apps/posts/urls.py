from django.urls import path
from . import views

urlpatterns = [
  path('', views.get_all, name='get_all'),
  path('<int:id>/', views.get, name='get_one'),
  path('delete/', views.delete, name='delete'),
  path('create/', views.create, name='create'),
  path('update/', views.update, name='update'),
]