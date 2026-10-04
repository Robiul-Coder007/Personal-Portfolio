from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'is_staff', 'is_active',)
    search_fields = ('username', 'email', 'full_name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'phone',)
    search_fields = ('user__username', 'user__full_name', 'designation',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'percentage',)
    list_filter = ('name',)
    search_fields = ('name', 'user__username',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree', 'institution', 'start_year', 'end_year',)
    search_fields = ('degree', 'institution', 'subject', 'user__username',)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'company', 'start_date', 'end_date', 'currently_working',)
    list_filter = ('currently_working',)
    search_fields = ('job_title', 'company', 'user__username',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at',)
    search_fields = ('title', 'technologies', 'user__username',)
    ordering = ('-created_at',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read',)
    list_filter = ('is_read', 'created_at',)
    search_fields = ('name', 'email', 'subject', 'message',)
    ordering = ('-created_at',)