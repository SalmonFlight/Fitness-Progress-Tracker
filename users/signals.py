from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, WeightEntry
from django.utils import timezone

#Create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#Save Profile when User is updated (only if profile exists)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver(post_save, sender=Profile)
def create_weight_entry(sender, instance, created, **kwargs):
    """Create a weight entry ONLY when profile is first created or weight changes."""
    
    # Skip if no weight
    if not instance.current_weight:
        return
    
    today = timezone.now().date()
    
    # Check if entry exists for today
    existing = WeightEntry.objects.filter(
        user=instance.user,
        date=today
    ).first()
    
    if existing:
        # Update if weight changed
        if existing.weight != instance.current_weight:
            existing.weight = instance.current_weight
            existing.save()
    else:
        # Create new entry
        WeightEntry.objects.create(
            user=instance.user,
            weight=instance.current_weight,
            date=today
        )