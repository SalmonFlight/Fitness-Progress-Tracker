from django.shortcuts import render, redirect
from django.views.generic import (CreateView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from fitnessapp.models import Exercise

class RegisterView(CreateView):
    """Handles user registration with email and password."""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        """Saves the new user and displays a success message."""
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Displays and updates the user's profile page.
    Handles two forms:
    - UserUpdateForm: Updates username and email
    - ProfileUpdateForm: Updates weight, height, weight unit, and tracked PRs
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        """Returns the currently logged-in user (the object being updated)."""
        return self.request.user
    
    def get_context_data(self, **kwargs):
        """
        Adds the profile form and exercise list to the template context.
        - If POST: Populates form with submitted data (for error display)
        - If GET: Populates form with existing profile data
        - exercises: All exercises for the PR selection checkboxes
        """
        context = super().get_context_data(**kwargs)
        
        # Populate profile form with existing data or POST data
        if self.request.method == 'POST':
            context['profile_form'] = ProfileUpdateForm(
                self.request.POST,
                instance=self.request.user.profile
            )
        else:
            context['profile_form'] = ProfileUpdateForm(
                instance=self.request.user.profile
            )
        
        # Pass all exercises for the "tracked PR exercises" checkboxes
        context['exercises'] = Exercise.objects.all().order_by('name')
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handles form submission.
        - Validates both forms
        - If valid: saves both and redirects to profile with success message
        - If invalid: re-renders the page with errors
        """
        self.object = self.get_object()
        form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        # If both forms are valid, save them
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        
        # If invalid, re-render the page with errors
        return render(request, self.template_name, {
            'form': form,
            'profile_form': profile_form,
            'exercises': Exercise.objects.all().order_by('name')
        })
        
@login_required
def set_theme(request):
    """Allows user to switch between dark and light theme"""
    if request.method == 'POST':
        theme = request.POST.get('theme')
        if theme in ['dark', 'light']:
            request.user.profile.theme = theme
            request.user.profile.save()
            request.session['theme'] = theme
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})