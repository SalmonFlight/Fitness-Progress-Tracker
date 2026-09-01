from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    # REQUIRED - Links to Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # REQUIRED FOR HOMEPAGE PR SECTION
    tracked_pr_exercises = models.JSONField(default=list)
    
    # DISPLAY PREFERENCES
    weight_unit = models.CharField(
        max_length=3,
        choices=[('kg', 'kg'), ('lbs', 'lbs')],
        default='kg'
    )
    
    # BODY STATS TRACKING
    current_weight = models.DecimalField(
        max_digits=5, 
        decimal_places=1, 
        null=True, 
        blank=True,
        help_text="Current body weight"
    )
    
    goal_weight = models.DecimalField(
        max_digits=5, 
        decimal_places=1, 
        null=True, 
        blank=True,
        help_text="Target body weight"
    )
    
    height = models.DecimalField(
        max_digits=5, 
        decimal_places=1, 
        null=True, 
        blank=True,
        help_text="Height in cm"
    )
          
    theme = models.CharField(max_length=10, choices=[('dark', 'Dark'), ('light', 'Light')], default='dark')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_entries')
    weight = models.DecimalField(max_digits=5, decimal_places=1)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username}: {self.weight}kg on {self.date}"
