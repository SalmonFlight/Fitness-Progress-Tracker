from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# Registration form with email field
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
        # Add placeholder text instead
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create a password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        # Django's validators will still run automatically
        # But errors will only show if there's a violation
        return password

# Form for updating username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    # Override the field to use MultipleChoiceField
    tracked_pr_exercises = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[]  # Will be set in __init__
    )
    
    class Meta:
        model = Profile
        fields = ['weight_unit', 'current_weight', 'goal_weight', 'height', 'tracked_pr_exercises']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set choices for tracked_pr_exercises from Exercise model
        from fitnessapp.models import Exercise
        exercises = Exercise.objects.all().order_by('name')
        self.fields['tracked_pr_exercises'].choices = [(ex.name, ex.name) for ex in exercises]
    
    def clean_current_weight(self):
        return self.cleaned_data.get('current_weight') or None
    
    def clean_goal_weight(self):
        return self.cleaned_data.get('goal_weight') or None
    
    def clean_height(self):
        return self.cleaned_data.get('height') or None