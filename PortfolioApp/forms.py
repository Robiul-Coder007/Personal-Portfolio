from django import forms
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Username",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Username"}))
    email = forms.EmailField(label="Email",required=True,widget=forms.EmailInput(attrs={"class": "form-control","placeholder": "Input Email"}))
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class": "form-control","placeholder": "Input Password"}))
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={"class": "form-control","placeholder": "Input Confirm Password"}))

    class Meta:
        model = CustomUser
        fields = ("username","email","password1","password2",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.lower()
            if CustomUser.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError("An account with this email already exists.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Username or Email"}))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class": "form-control","placeholder": "Input Password"}))

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username_or_email and password:
            if '@' in username_or_email:
                try:
                    user_obj = CustomUser.objects.get(
                        email__iexact=username_or_email
                    )
                    username = user_obj.username
                except CustomUser.DoesNotExist:
                    raise forms.ValidationError("Invalid username or email.")
            else:
                username = username_or_email
            self.user_cache = authenticate(
                self.request,
                username=username, 
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError("Invalid username/email or password.")
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password",widget=forms.PasswordInput(attrs={"class": "form-control","placeholder": "Input Old Password"}))
    new_password1 = forms.CharField(label="New Password",widget=forms.PasswordInput(attrs={"class": "form-control","placeholder": "Input New Password"}))
    new_password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={"class": "form-control","placeholder": "Input Confirm Password"}))

class ProfileForm(forms.ModelForm):
    name = forms.CharField(label="Name",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Name"}))
    father_name = forms.CharField(label="Father’s Name",required=False,widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Father’s Name"}))
    mother_name = forms.CharField(label="Mother’s Name",required=False,widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Mother’s Name"}))
    email = forms.EmailField(label="Email",widget=forms.EmailInput(attrs={"class": "form-control","placeholder": "Input Email"}))
    phone = forms.CharField(label="Phone Number",required=False,widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Phone Number","type": "tel"}))
    mailing_address = forms.CharField(label="Mailing Address",required=False,widget=forms.TextInput(attrs={"class": "form-control","rows": 3,"placeholder": "Input Mailing Address"}))
    permanent_address = forms.CharField(label="Permanent Address",required=False,widget=forms.TextInput(attrs={"class": "form-control","rows": 3,"placeholder": "Input Permanent Address"}))
    date_of_birth = forms.DateField(label="Date of Birth",required=False,widget=forms.DateInput(attrs={"class": "form-control","type": "date"}))
    nationality = forms.CharField(label="Nationality",required=False,widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Nationality"}))
    religion = forms.CharField(label="Religion",required=False,widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Religion"}))
    marital_status = forms.CharField(label="Marital Status",required=False,widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Marital Status"}))
    gender = forms.ChoiceField(label="Gender",required=False,choices=[("","Select Gender"), ("Male","Male"), ("Female","Female")],widget=forms.Select(attrs={"class": "form-control"}))
    career_objective = forms.CharField(label="Career Objective",required=False,widget=forms.TextInput(attrs={"class": "form-control","rows": 5,"placeholder": "Input Career Objective"}))
    interests = forms.CharField(label="Interests",required=False,widget=forms.TextInput(attrs={"class": "form-control","rows": 3,"placeholder": "Input Interests"}))
    profile_image = forms.ImageField(label="Profile Picture",required=False,widget=forms.ClearableFileInput(attrs={"class": "form-control"}))

    class Meta:
        model = Profile
        fields = ["name","father_name","mother_name","email","phone","mailing_address","permanent_address","date_of_birth","nationality","religion","marital_status","gender","career_objective","interests","profile_image",]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return email
        email = email.lower()
        queryset = Profile.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError("This email is already used by another profile.")
        return email

class SkillForm(forms.ModelForm):
    name = forms.CharField(label="Name",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Name"}))
    category = forms.CharField(label="Category",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Category"}))
    proficiency = forms.IntegerField(label="Proficiency",widget=forms.NumberInput(attrs={"class": "form-control","min": 0,"max": 100,"placeholder": "Input Proficiency 0 - 100"}))
    description = forms.CharField(label="Description",widget=forms.Textarea(attrs={"class": "form-control","rows": 4,"placeholder": "Input Skill Description"}))

    class Meta:
        model = Skill
        fields = ["name","category","proficiency","description",]

    def clean_proficiency(self):
        proficiency = self.cleaned_data.get("proficiency")
        if proficiency is not None:
            if proficiency < 0 or proficiency > 100:
                raise forms.ValidationError("Proficiency must be between 0 and 100.")
        return proficiency

class EducationForm(forms.ModelForm):
    qualification = forms.CharField(label="Qualification",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Qualification"}))
    institute = forms.CharField(label="Institute",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Institute Name"}))
    group_or_subject = forms.CharField(label="Group / Subject",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Group / Subject"}))
    result_or_cgpa = forms.FloatField(label="Result / CGPA",widget=forms.NumberInput(attrs={"class": "form-control","placeholder": "Input Result / CGPA"}))
    board = forms.CharField(label="Board",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Board"}))
    passing_year = forms.IntegerField(label="Passing Year",widget=forms.NumberInput(attrs={"class": "form-control","placeholder": "Input Passing Year"}))
    description = forms.CharField(label="Description",widget=forms.Textarea(attrs={"class": "form-control","rows": 4,"placeholder": "Input Education Description"}))

    class Meta:
        model = Education
        fields = ["qualification","institute","group_or_subject","result_or_cgpa","board","passing_year","description",]

class ExperienceForm(forms.ModelForm):
    job_title = forms.CharField(label="Job Title",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Job Title"}))
    company_name = forms.CharField(label="Company Name",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Company Name"}))
    location = forms.CharField(label="Location",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Job Location"}))
    start_date = forms.DateField(label="Start Date",widget=forms.DateInput(attrs={"class": "form-control","placeholder": "Input Start Date","type": "date"}))
    end_date = forms.DateField(label="End Date",widget=forms.DateInput(attrs={"class": "form-control","placeholder": "Input End Date","type": "date"}))
    currently_working = forms.BooleanField(label="Currently Working",required=False,widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    description = forms.CharField(label="Description",widget=forms.Textarea(attrs={"class": "form-control","rows": 5,"placeholder": "Input Job Responsibilities and Achievements"}))

    class Meta:
        model = Experience
        fields = ["job_title","company_name","location","start_date","end_date","currently_working","description",]

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        currently_working = cleaned_data.get("currently_working")
        if currently_working:
            cleaned_data["end_date"] = None
        else:
            if start_date and end_date and end_date < start_date:
                self.add_error('end_date', "End date cannot be earlier than start date.")
        return cleaned_data

class ProjectForm(forms.ModelForm):
    title = forms.CharField(label="Project Title",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Project Title"}))
    description = forms.CharField(label="Description",widget=forms.Textarea(attrs={"class": "form-control","rows": 6,"placeholder": "Input Project Description"}))
    technologies = forms.CharField(label="Technologies",required=False,widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Technologies Example: Python, Django, HTML, CSS"}))
    github_url = forms.URLField(label="GitHub URL",required=False,widget=forms.URLInput(attrs={"class": "form-control","placeholder": "https://github.com/username/project"}))
    image = forms.ImageField(label="Project Image",required=False,widget=forms.ClearableFileInput(attrs={"class": "form-control","accept": "image/*"}))
    is_featured = forms.BooleanField(label="Featured Project",required=False,widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    class Meta:
        model = Project
        fields = ["title","description","technologies","github_url","image","is_featured",]

class ContactMessageForm(forms.ModelForm):
    profile = forms.ModelChoiceField(label="Select Portfolio Profile",queryset=Profile.objects.all().order_by("name"),
                                    empty_label="--- Select a Profile ---",widget=forms.Select(attrs={"class": "form-select","id": "id_profile",}))
    name = forms.CharField(label="Your Name",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Your Name"}))
    email = forms.EmailField(label="Your Email",widget=forms.EmailInput(attrs={"class": "form-control","placeholder": "Input Your Email"}))
    subject = forms.CharField(label="Subject",widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Input Subject"}))
    message = forms.CharField(label="Message",widget=forms.Textarea(attrs={"class": "form-control","rows": 6,"placeholder": "Write your message..."}))

    class Meta:
        model = ContactMessage
        fields = ["profile","name","email","subject","message",]

    def __init__(self, *args, **kwargs):
        super(ContactMessageForm, self).__init__(*args, **kwargs)
        profile_choices = [(profile.id, profile.name) for profile in Profile.objects.all()]
        profile_choices.insert(0, ('', '--- Select a Profile ---'))
        self.fields['profile'].choices = profile_choices

    def clean_profile(self):
        profile_data = self.cleaned_data.get('profile')
        if isinstance(profile_data, Profile):
            return profile_data
        if profile_data:
            try:
                return Profile.objects.get(id=profile_data)
            except (Profile.DoesNotExist, ValueError, TypeError):
                raise forms.ValidationError("Selected profile does not exist.")
        return None