from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import *

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Input Username'}))
    full_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Full Name'}))
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Input Email'}))
    pro_pic = forms.ImageField(label='Profile Picture', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input Password'}))
    password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input Confirm Password'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'password1', 'password2', 'pro_pic',]

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Username or Email'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input Password'}))

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username_or_email and password:
            if '@' in username_or_email:
                try:
                    user_obj = CustomUser.objects.get(email=username_or_email)
                    username = user_obj.username
                except CustomUser.DoesNotExist:
                    raise forms.ValidationError("Invalid username or email.")
            else:
                username = username_or_email
            self.cleaned_data['username'] = username
            return super().clean()
        return self.cleaned_data

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input Old Password'}))
    new_password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input New Password'}))
    new_password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Input Confirm Password'}))

class ProfileForm(forms.ModelForm):
    designation = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Designation'}))
    biography = forms.CharField(label="",widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Input Biography', 'rows': 4}))
    phone = forms.CharField(label="",required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Phone Number', 'type': 'tel'}))
    address = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Address'}))
    github = forms.URLField(label="",widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Input GitHub URL'}))
    linkedin = forms.URLField(label="",widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Input LinkedIn URL'}))
    facebook = forms.URLField(label="",widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Input Facebook URL'}))
    date_of_birth = forms.DateField(label="",widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    class Meta:
        model = Profile
        fields = ['designation', 'biography', 'phone', 'address', 'github', 'linkedin', 'facebook', 'date_of_birth',]

class SkillForm(forms.ModelForm):
    name = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Skill Name'}))
    percentage = forms.IntegerField(label="",widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Percentage 0 - 100', 'min': 0, 'max': 100}))
    class Meta:
        model = Skill
        fields = ['name', 'percentage',]

class EducationForm(forms.ModelForm):
    degree = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Degree'}))
    institution = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Institution'}))
    subject = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Subject'}))
    start_year = forms.IntegerField(label="",widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Input Start Year'}))
    end_year = forms.IntegerField(label="",widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Input End Year'}))
    description = forms.CharField(label="",widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Input Description', 'rows': 4}))
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'subject', 'start_year', 'end_year', 'description',]

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_year')
        end = cleaned_data.get('end_year')
        if start and end and end < start:
            raise forms.ValidationError('End year cannot be before start year.')
        return cleaned_data

class ExperienceForm(forms.ModelForm):
    job_title = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Job Title'}))
    company = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Company'}))
    start_date = forms.DateField(label="",widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(required=False,label="",widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    description = forms.CharField(label="",widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Input Description', 'rows': 4}))
    currently_working = forms.BooleanField(required=False,label="Currently Working Here",widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    class Meta:
        model = Experience
        fields = ['job_title', 'company', 'start_date', 'end_date', 'description', 'currently_working',]

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        current = cleaned_data.get('currently_working')
        if start and end and end < start:
            raise forms.ValidationError('End date cannot be before start date.')
        if current:
            cleaned_data['end_date'] = None
        return cleaned_data

class ProjectForm(forms.ModelForm):
    title = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Project Title'}))
    description = forms.CharField(label="",widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Input Project Description', 'rows': 4}))
    technologies = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Technologies - Python, Django, HTML, CSS'}))
    github_url = forms.URLField(required=False,label="",widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Input GitHub Repository URL'}))
    image = forms.ImageField(required=False,label="Project Image", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies', 'github_url', 'image',]

class ContactMessageForm(forms.ModelForm):
    name = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Your Name'}))
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Input Your Email'}))
    subject = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Subject'}))
    message = forms.CharField(label="",widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Input Message', 'rows': 4}))
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message',]