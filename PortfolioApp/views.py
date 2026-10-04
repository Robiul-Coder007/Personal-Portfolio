from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import *
from .forms import *

def home(request):
    profile = Profile.objects.all().first()
    skills = Skill.objects.all().order_by('-percentage')
    educations = Education.objects.all().order_by('-start_year')
    experiences = Experience.objects.all().order_by('-start_date')
    projects = Project.objects.all().order_by('-created_at')
    contact_form = ContactMessageForm()
    context = {
        'page': 'Home',
        'profile': profile,
        'skills': skills,
        'educations': educations,
        'experiences': experiences,
        'projects': projects,
        'contact_form': contact_form,
    }
    return render(request, 'home.html', context)

def resume(request):
    profile = Profile.objects.select_related('user').first()

    skills = Skill.objects.all().order_by('-percentage')
    educations = Education.objects.all().order_by('-start_year')
    experiences = Experience.objects.all().order_by('-start_date')
    projects = Project.objects.all().order_by('-created_at')

    context = {
        'page': 'CV / Resume',
        'profile': profile,
        'skills': skills,
        'educations': educations,
        'experiences': experiences,
        'projects': projects,
    }
    return render(request, 'resume.html', context)

def user_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('user_login')
    else:
        form = RegistrationForm()
    return render(request, 'user_register.html', {'page' : 'User Registration', 'form' : form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.full_name or user.username}!')
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'user_login.html', {'page' : 'User Login', 'form' : form})

@login_required(login_url='user_login')
def update_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'page' : 'Update Profile', 'form' : form})

@login_required(login_url='user_login')
def change_pass(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password is successfully updated!')
            return redirect('dashboard')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'change_pass.html', {'page' : 'Change Password', 'form' : form})

@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url='user_login')
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    skills = Skill.objects.filter(user=request.user)
    educations = Education.objects.filter(user=request.user)
    experiences = Experience.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user)
    messages_list = ContactMessage.objects.filter()
    context = {
        'page': 'Dashboard',
        'profile': profile,
        'skills': skills,
        'educations': educations,
        'experiences': experiences,
        'projects': projects,
        'messages_list': messages_list,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='user_login')
def skill_create(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, 'Skill created successfully.')
            return redirect('skill_list')
    else:
        form = SkillForm()
    return render(request, 'skill_create.html', {'page' : 'Create Skill', 'form' : form})

@login_required(login_url='user_login')
def skill_list(request):
    skills = Skill.objects.filter(user=request.user)
    return render(request, 'skill_list.html', {'page' : 'Skill List', 'skills' : skills})

@login_required(login_url='user_login')
def skill_update(request, id):
    skill = get_object_or_404(Skill, id=id, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully.')
            return redirect('skill_list')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'skill_update.html', {'page' : 'Update Skill', 'form' : form})

@login_required(login_url='user_login')
def skill_delete(request, id):
    skill = get_object_or_404(Skill, id=id, user=request.user)
    skill.delete()
    messages.success(request, 'Skill deleted successfully.')
    return redirect('skill_list')

@login_required(login_url='user_login')
def education_create(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            messages.success(request, 'Education added successfully.')
            return redirect('education_list')
    else:
        form = EducationForm()
    return render(request, 'education_create.html', {'page' : 'Create Education', 'form' : form})

@login_required(login_url='user_login')
def education_list(request):
    educations = Education.objects.filter(user=request.user)
    return render(request, 'education_list.html', {'page' : 'Education List', 'educations' : educations})

@login_required(login_url='user_login')
def education_update(request, id):
    education = get_object_or_404(Education, id=id, user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, 'Education updated successfully.')
            return redirect('education_list')
    else:
        form = EducationForm(instance=education)
    return render(request, 'education_update.html', {'page' : 'Update Education', 'form' : form})

@login_required(login_url='user_login')
def education_delete(request, id):
    education = get_object_or_404(Education, id=id, user=request.user)
    education.delete()
    messages.success(request, 'Education deleted successfully.')
    return redirect('education_list')

@login_required(login_url='user_login')
def experience_create(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            messages.success(request, 'Experience added successfully.')
            return redirect('experience_list')
    else:
        form = ExperienceForm()
    return render(request, 'experience_create.html', {'page' : 'Create Experience', 'form' : form})

@login_required(login_url='user_login')
def experience_list(request):
    experiences = Experience.objects.filter(user=request.user)
    return render(request, 'experience_list.html', {'page' : 'Experience List', 'experiences' : experiences})

@login_required(login_url='user_login')
def experience_update(request, id):
    experience = get_object_or_404(Experience, id=id, user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experience updated successfully.')
            return redirect('experience_list')
    else:
        form = ExperienceForm(instance=experience)
    return render(request, 'experience_update.html', {'page' : 'Update Experience', 'form' : form})

@login_required(login_url='user_login')
def experience_delete(request, id):
    experience = get_object_or_404(Experience, id=id, user=request.user)
    experience.delete()
    messages.success(request, 'Experience deleted successfully.')
    return redirect('experience_list')

@login_required(login_url='user_login')
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, 'Project added successfully.')
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_create.html', {'page' : 'Create Project', 'form' : form})

@login_required(login_url='user_login')
def project_list(request):
    projects = Project.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'project_list.html', {'page' : 'Project List', 'projects' : projects})

@login_required(login_url='user_login')
def project_update(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_update.html', {'page' : 'Update Project', 'form' : form})

@login_required(login_url='user_login')
def project_delete(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    project.delete()
    messages.success(request, 'Project deleted successfully.')
    return redirect('project_list')

def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactMessageForm()
    return render(request, 'contact.html', {'page' : 'Contact', 'form' : form})

@login_required(login_url='user_login')
def contact_messages(request):
    messages_list = ContactMessage.objects.all()
    return render(request, 'contact_messages.html', {'page' : 'Contact Messages', 'messages_list' : messages_list})

@login_required(login_url='user_login')
def contact_message_detail(request, id):
    message = get_object_or_404(ContactMessage, id=id)
    message.is_read = True
    message.save()
    return render(request, 'contact_message_detail.html', {'page' : 'Contact Message Detail', 'message' : message})

@login_required(login_url='user_login')
def contact_message_delete(request, id):
    message = get_object_or_404(ContactMessage, id=id)
    message.delete()
    messages.success(request, 'Message deleted successfully.')
    return redirect('contact_messages')