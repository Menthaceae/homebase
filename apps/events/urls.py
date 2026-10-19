from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_event, name='create_event'),
    path('all/', views.view_all, name='view_all_events'),
]