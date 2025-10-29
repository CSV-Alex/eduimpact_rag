from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<int:project_id>/chat/', views.chat_interface, name='chat_interface'),
    path('project/<int:project_id>/message/', views.chat_message, name='chat_message'),
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
]