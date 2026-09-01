from django.contrib import admin
from .models import Exercise, Workout, Set, PersonalRecord

admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(Set)
admin.site.register(PersonalRecord)
