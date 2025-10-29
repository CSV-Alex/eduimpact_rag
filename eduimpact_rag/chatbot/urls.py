from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<int:project_id>/chat/', views.chat_interface, name='chat_interface'),
    path('project/<int:project_id>/message/', views.chat_message, name='chat_message'),
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:project_id>/resources/', views.resources_dashboard, name='resources_dashboard'),
    path('project/<int:project_id>/generate_lesson_plan/', views.generate_lesson_plan, name='generate_lesson_plan'),
    path('project/<int:project_id>/generate_student_tracker/', views.generate_student_tracker, name='generate_student_tracker'),
    path('project/<int:project_id>/generate_gamification_template/', views.generate_gamification_template, name='generate_gamification_template'),

]