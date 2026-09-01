from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('CHEST', 'Chest'),
        ('BACK', 'Back'),
        ('LEGS', 'Legs'),
        ('SHOULDERS', 'Shoulders'),
        ('ARMS', 'Arms'),
        ('CORE', 'Core'),
        ('CARDIO', 'Cardio'),
        ('FULL_BODY', 'Full Body'),
    ]
    name = models.CharField(max_length = 100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_custom = models.BooleanField(default=False)
    
    #Admin display Feature
    def __str__(self):
        return f"{self.name}"  
    
    #Orders Exercises by Alphabetical order of exercise name
    class Meta:
        ordering = ['name']
    
class Workout(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('completed', 'Completed'),
    ]
    
    name = models.CharField(max_length = 100)
    duration = models.PositiveSmallIntegerField(help_text="Duration in minutes")
    date = models.DateTimeField(default = timezone.now)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    notes = models.TextField(blank = True, null = True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    class Meta:
        ordering = ['-date']  # Sort by newest first
    
    def __str__(self):
        return f"{self.name} - {self.date.strftime('%b %d, %Y')}"  # For admin site display
    
    @property
    def total_volume(self):
        """Calculate total volume for this workout"""
        return sum(set.total_volume for set in self.sets.all())
    
    def is_completed(self):
        """Check if workout is completed"""
        return self.status == 'completed'
    
    def is_draft(self):
        """Check if workout is a draft"""
        return self.status == 'draft'

class Set(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name = 'sets')
    exercise = models.ForeignKey(Exercise, on_delete = models.CASCADE)
    set_count = models.PositiveSmallIntegerField(help_text="amount of sets")
    reps = models.PositiveSmallIntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2) # in kg
    order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.exercise.name}: {self.set_count}x{self.reps} reps @ {self.weight}kg"
    
    @property
    def total_volume(self):
        """Calculate total volume: sets × reps × weight"""
        return self.set_count * self.reps * self.weight
      
class PersonalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE, null=True, blank=True)  
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    reps = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-weight']
    
    def __str__(self):
        return f"{self.exercise.name}: {self.weight}kg × {self.reps} reps"
    