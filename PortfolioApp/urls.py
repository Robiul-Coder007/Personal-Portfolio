from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('resume/', resume, name='resume'),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('change-password/', change_pass, name='change_pass'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/profile/', update_profile, name='update_profile'),

    path('dashboard/skills/', skill_list, name='skill_list'),
    path('dashboard/skills/create/', skill_create, name='skill_create'),
    path('dashboard/skills/<int:id>/update/', skill_update, name='skill_update'),
    path('dashboard/skills/<int:id>/delete/', skill_delete, name='skill_delete'),

    path('dashboard/education/', education_list, name='education_list'),
    path('dashboard/education/create/', education_create, name='education_create'),
    path('dashboard/education/<int:id>/update/', education_update, name='education_update'),
    path('dashboard/education/<int:id>/delete/', education_delete, name='education_delete'),

    path('dashboard/experience/', experience_list, name='experience_list'),
    path('dashboard/experience/create/', experience_create, name='experience_create'),
    path('dashboard/experience/<int:id>/update/', experience_update, name='experience_update'),
    path('dashboard/experience/<int:id>/delete/', experience_delete, name='experience_delete'),

    path('dashboard/projects/', project_list, name='project_list'),
    path('dashboard/projects/create/', project_create, name='project_create'),
    path('dashboard/projects/<int:id>/update/', project_update, name='project_update'),
    path('dashboard/projects/<int:id>/delete/', project_delete, name='project_delete'),

    path('contact/', contact, name='contact'),
    path('contact/messages/', contact_messages, name='contact_messages'),
    path('contact/messages/<int:id>/', contact_message_detail, name='contact_message_detail'),
    path('contact/messages/<int:id>/delete/', contact_message_delete, name='contact_message_delete'),
]