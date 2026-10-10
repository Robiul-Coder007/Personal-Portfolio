from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username","email",)
    search_fields = ("username","email",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name","email","phone","nationality","created_at",)
    search_fields = ("name","email","phone",)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name","category","proficiency","profile",)
    list_filter = ("category",)
    search_fields = ("name","category","profile__name",)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("qualification","institute","result_or_cgpa","board","passing_year","profile",)
    list_filter = ("board","passing_year",)
    search_fields = ("qualification","institute","group_or_subject","profile__name",)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("job_title","company_name","start_date","end_date","currently_working","profile",)
    list_filter = ("currently_working",)
    search_fields = ("job_title","company_name","profile__name",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title","profile","is_featured","created_at",)
    list_filter = ("is_featured",)
    search_fields = ("title","technologies","profile__name",)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("profile","name","email","subject","is_read","created_at",)
    list_filter = ("is_read","created_at",)
    search_fields = ("profile","name","email","subject","message",)
    readonly_fields = ("created_at",)