from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import path, include
from users import views as user_views

urlpatterns = [
     #admin panel
    path('admin/', admin.site.urls),
    
    #Directs to fitnessapp urls.py
    path('', include('fitnessapp.urls')),  
    
    #Authentication URLs
    path('register/', user_views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    #Password Reset Urls
    path('password-reset/', 
         PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', 
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', 
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/', 
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    
    # Profile
    path('profile/', user_views.ProfileView.as_view(), name='profile'),
    
    #Dark and Light Mode
    path('set-theme/', user_views.set_theme, name='set_theme'),
]
