from django import forms
from .models import Workout, Set

"""Adds additional parameters to be filled in"""


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'date', 'duration', 'notes']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['set_count', 'reps', 'weight']
        widgets = {
            'set_count': forms.NumberInput(attrs={'min': 1}),
            'reps': forms.NumberInput(attrs={'min': 1}),
            'weight': forms.NumberInput(attrs={'min': 0, 'step': 0.5}),
        }