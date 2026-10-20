from django.urls import path

from . import views

# messages/
urlpatterns = [
  path('', views.get_all_message_groups, name='get_all_message_groups'),
  path('groups/create/',views.create_message_group, name='make_group'),
  path('groups/<int:message_group_id>/send/', views.send_message, name='send_message'),
  path('groups/<int:message_group_id>/', views.get_all_messages, name='get_all_messages')
]