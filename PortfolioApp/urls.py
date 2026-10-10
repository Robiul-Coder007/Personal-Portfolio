from django.urls import path
from .views import *

urlpatterns = [
    path("registration/", user_register, name="user_register"),
    path("login/", user_login, name="user_login"),
    path("change-password/", change_pass, name="change_pass"),
    path("logout/", user_logout, name="user_logout"),

    path('resume/<int:profile_id>/', resume, name='resume'),
    path("dashboard/", dashboard, name="dashboard"),
    path("profile/update/", update_profile, name="update_profile",),

    path("skills/create/", skill_create, name="skill_create"),
    path("skills/list/", skill_list, name="skill_list"),
    path("skills/<int:pk>/update/", skill_update, name="skill_update"),
    path("skills/<int:pk>/delete/", skill_delete, name="skill_delete"),

    path("education/create/", education_create, name="education_create"),
    path("education/list/", education_list, name="education_list"),
    path("education/<int:pk>/update/", education_update, name="education_update"),
    path("education/<int:pk>/delete/", education_delete, name="education_delete"),
    
    path("experience/create/", experience_create, name="experience_create"),
    path("experience/list/", experience_list, name="experience_list"),
    path("experience/<int:pk>/update/", experience_update, name="experience_update"),
    path("experience/<int:pk>/delete/", experience_delete, name="experience_delete"),

    path("projects/create/", project_create, name="project_create"),
    path("projects/list/", project_list, name="project_list"),
    path("projects/<int:pk>/update/", project_update, name="project_update"),
    path("projects/<int:pk>/delete/", project_delete, name="project_delete"),

    path("", contact, name="contact"),
    path("contact-messages/list/", contact_messages, name="contact_messages"),
    path("contact-messages/<int:pk>/detail/", contact_message_detail, name="contact_message_detail"),
    path("contact-messages/<int:pk>/read/", contact_message_read, name="contact_message_read"),
    path("contact-messages/<int:pk>/delete/", contact_message_delete, name="contact_message_delete"),
]