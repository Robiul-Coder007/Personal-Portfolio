from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import *
from .forms import *

def user_register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )
            login(request, user)
            messages.success(request,
                f"""Registration successful.
                Your profile has been created and logged."""
            )
            return redirect("dashboard")
    else:
        form = RegistrationForm()
    return render(request, "user_register.html", {"page": "User Registration","form": form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, "user_login.html", {"page": "User Login","form": form})

@login_required(login_url=user_login)
def change_pass(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password is successfully changed! Please login again.")
            return redirect("user_login")
    else:
        form = ChangePasswordForm(request.user)
    return render(request, "change_pass.html", {"page": "Change Password","form": form})

@login_required(login_url=user_login)
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("user_login")

@login_required(login_url=user_login)
def dashboard(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username,
            "email": request.user.email,
        }
    )
    skill = Skill.objects.filter(profile=profile).count()
    education = Education.objects.filter(profile=profile).count()
    experience = Experience.objects.filter(profile=profile).count()
    project = Project.objects.filter(profile=profile).count()
    contact_message_count = ContactMessage.objects.filter(profile=profile).count()
    unread_message_count = ContactMessage.objects.filter(profile=profile, is_read=False).count()
    context = {
        "page": "Dashboard",
        "profile": profile,
        "profile_created": created,
        "skill_count": skill,
        "education_count": education,
        "experience_count": experience,
        "project_count": project,
        "contact_message_count": contact_message_count,
        "unread_message_count": unread_message_count
    }
    return render(request, "dashboard.html", context)

@login_required(login_url=user_login)
def update_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username,
            "email": request.user.email,
        }
    )
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)
    context = {
        "page": "Update Profile",
        "profile": profile,
        "profile_created": created,
        "form": form,
    }
    return render(request, "update_profile.html", context)

@login_required(login_url=user_login)
def skill_create(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = profile
            skill.save()
            messages.success(request, "Skill created successfully.")
            return redirect("skill_list")
    else:
        form = SkillForm()
    context = {
        "page": "Add Skill",
        "form": form,
        "title": "Add Skill",
        "button_text": "Save Skill"
    }
    return render(request, "skill_form.html", context)

@login_required(login_url=user_login)
def skill_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    skills = Skill.objects.filter(profile=profile)
    return render(request, "skill_list.html", {"page": "Skills","skills": skills})

@login_required(login_url=user_login)
def skill_update(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    skill = get_object_or_404(Skill, pk=pk, profile=profile)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully.")
            return redirect("skill_list")
    else:
        form = SkillForm(instance=skill)
    context = {
        "page": "Update Skill",
        "form": form,
        "title": "Update Skill",
        "button_text": "Update Skill"
    }
    return render(request, "skill_form.html", context)

@login_required(login_url=user_login)
def skill_delete(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    skill = get_object_or_404(Skill, pk=pk, profile=profile)
    skill.delete()
    messages.success(request, "Skill deleted successfully.")
    return redirect("skill_list")

@login_required(login_url=user_login)
def education_create(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.profile = profile
            education.save()
            messages.success(request, "Education created successfully.")
            return redirect("education_list")
    else:
        form = EducationForm()
    context = {
        "page": "Add Education",
        "form": form,
        "title": "Add Education",
        "button_text": "Save Education"
    }
    return render(request, "education_form.html", context)

@login_required(login_url=user_login)
def education_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    educations = Education.objects.filter(profile=profile)
    return render(request, "education_list.html", {"page": "Education","educations": educations})

@login_required(login_url=user_login)
def education_update(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    education = get_object_or_404(Education, pk=pk, profile=profile)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, "Education updated successfully.")
            return redirect("education_list")
    else:
        form = EducationForm(instance=education)
    context = {
        "page": "Update Education",
        "form": form,
        "title": "Update Education",
        "button_text": "Update Education",
    }
    return render(request, "education_form.html", context)

@login_required(login_url=user_login)
def education_delete(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    education = get_object_or_404(Education, pk=pk, profile=profile)
    education.delete()
    messages.success(request, "Education deleted successfully.")
    return redirect("education_list")

@login_required(login_url=user_login)
def experience_create(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.profile = profile
            experience.save()
            messages.success(request, "Experience created successfully.")
            return redirect("experience_list")
    else:
        form = ExperienceForm()
    context = {        
        "page": "Add Experience",
        "form": form,
        "title": "Add Experience",
        "button_text": "Save Experience",
    }
    return render(request, "experience_form.html", context)

@login_required(login_url=user_login)
def experience_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    experiences = Experience.objects.filter(profile=profile)
    return render(request, "experience_list.html", {"page": "Experience","experiences": experiences})

@login_required(login_url=user_login)
def experience_update(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    experience = get_object_or_404(Experience, pk=pk, profile=profile)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience updated successfully.")
            return redirect("experience_list")
    else:
        form = ExperienceForm(instance=experience)
    context = {
        "page": "Update Experience",
        "form": form,
        "title": "Update Experience",
        "button_text": "Update Experience",
    }
    return render(request, "experience_form.html", context)

@login_required(login_url=user_login)
def experience_delete(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    experience = get_object_or_404(Experience, pk=pk, profile=profile)
    experience.delete()
    messages.success(request, "Experience deleted successfully.")
    return redirect("experience_list")

@login_required(login_url=user_login)
def project_create(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = profile
            project.save()
            messages.success(request, "Project created successfully.")
            return redirect("project_list")
    else:
        form = ProjectForm()
    context = {
        "page": "Add Project",
        "form": form,
        "title": "Add Project",
        "button_text": "Save Project",
    }
    return render(request, "project_form.html", context)

@login_required(login_url=user_login)
def project_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    projects = Project.objects.filter(profile=profile)
    return render(request, "project_list.html", {"page": "Projects","projects": projects})

@login_required(login_url=user_login)
def project_update(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    project = get_object_or_404(Project, pk=pk, profile=profile)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully.")
            return redirect("project_list")
    else:
        form = ProjectForm(instance=project)
    context = {
        "page": "Update Project",
        "form": form,
        "project": project,
        "title": "Update Project",
        "button_text": "Update Project",
    }
    return render(request, "project_form.html", context)

@login_required(login_url=user_login)
def project_delete(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    project = get_object_or_404(Project, pk=pk, profile=profile)
    project.delete()
    messages.success(request, "Project deleted successfully.")
    return redirect("project_list")

def contact(request):
    profiles = Profile.objects.all().order_by("name")
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.profile = form.cleaned_data["profile"]
            contact_message.is_read = False
            contact_message.save()
            messages.success(request, "Your message has been sent to the selected profile.")
            return redirect("contact")
    else:
        form = ContactMessageForm()
    context = {
        "page": "Contact Profiles",
        "form": form,
        "profiles": profiles,
    }
    return render(request, "contact.html", context)

def resume(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    skills = Skill.objects.filter(profile=profile)
    educations = Education.objects.filter(profile=profile)
    experiences = Experience.objects.filter(profile=profile)
    projects = Project.objects.filter(profile=profile)
    context = {
        "page": f"{profile.name} - CV / Resume",
        "profile": profile,
        "skills": skills,
        "educations": educations,
        "experiences": experiences,
        "projects": projects,
    }
    return render(request, "resume.html", context)

@login_required(login_url=user_login)
def contact_messages(request):
    profile = get_object_or_404(Profile, user=request.user)
    contact_message_list = ContactMessage.objects.filter(profile=profile)
    return render(request, "contact_messages.html", {"page": "Contact Messages","contact_messages": contact_message_list})

@login_required(login_url=user_login)
def contact_message_detail(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    contact_message = get_object_or_404(ContactMessage, pk=pk, profile=profile)
    return render(request, "contact_message_detail.html", {"page": "Message Details","contact_message": contact_message})

@login_required(login_url=user_login)
def contact_message_read(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    contact_message = get_object_or_404(ContactMessage, pk=pk, profile=profile)
    if request.method == "POST":
        contact_message.is_read = not contact_message.is_read
        contact_message.save(update_fields=["is_read"])
        if contact_message.is_read:
            messages.success(request, "Message marked as read.")
        else:
            messages.success(request, "Message marked as unread.")
    return redirect("contact_messages")

@login_required(login_url=user_login)
def contact_message_delete(request, pk):
    profile = get_object_or_404(Profile, user=request.user)
    contact_message = get_object_or_404(ContactMessage, pk=pk, profile=profile)
    contact_message.delete()
    messages.success(request, "Contact message deleted successfully.")
    return redirect("contact_messages")