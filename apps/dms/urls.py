from django.urls import path

from . import views

# messages/
urlpatterns = [
  path('', views.view_all_messages, name='view_all_messages'),
  path('chat/create/',views.create_group_chat, name='create_group_chat'),
  path('groups/<int:message_group_id>/', views.get_all_messages, name='get_all_messages'),
  path('groups/<int:message_group_id>/invite/', views.invite, name='invite'),
  path('users/', views.list_all_users, name='list_all_users'),
]