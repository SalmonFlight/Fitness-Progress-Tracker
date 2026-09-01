from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Set, PersonalRecord

@receiver(post_save, sender=Set)
def detect_personal_record(sender, instance, created, **kwargs):
    """
    Auto-detects Personal Records (PRs) when a new Set is saved.
    If the set's weight is higher than the user's previous best,
    a new PersonalRecord entry is created.
    """
    # Only run for new sets (not updates)
    if not created:
        return
    
    # Get the workout and user
    workout = instance.workout
    user = workout.user
    
    # Only detect PRs for completed workouts
    if workout.status != 'completed':
        return
    
    # Find the user's current best for this exercise
    previous_pr = PersonalRecord.objects.filter(
        user=user,
        exercise=instance.exercise
    ).order_by('-weight').first()
    
    # If no PR exists, or this set is heavier, create a new PR
    if not previous_pr or instance.weight > previous_pr.weight:
        PersonalRecord.objects.create(
            user=user,
            exercise=instance.exercise,
            workout=workout,  # Link back to the workout that created it
            weight=instance.weight,
            reps=instance.reps,
            date=workout.date.date()
        )