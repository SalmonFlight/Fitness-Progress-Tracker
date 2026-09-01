from django.contrib import admin
from .models import Profile, WeightEntry

@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_weight', 'goal_weight', 'height']
    
    def save_model(self, request, obj, form, change):
        obj._skip_signal = True
        super().save_model(request, obj, form, change)

@admin.register(WeightEntry)
class WeightEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight', 'date']
    list_filter = ['user']
    search_fields = ['user__username']
    ordering = ['-date']