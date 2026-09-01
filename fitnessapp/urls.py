from django.urls import path
from .views import (
     HomePageView,
     ExerciseCatalogView,
     WorkoutCreateView,
     WorkoutDetailView,
     WorkoutHistoryView,
     WorkoutDeleteView,
     DraftListView,
     DraftUpdateView,
     DraftDeleteView,
     DraftAddExercisesView,
)

urlpatterns = [
     #Home Page (dashboard)
     path('home/', HomePageView.as_view(), name='home'),
     
     #Exercise Catalog
     path('workout/select/', ExerciseCatalogView.as_view(), name='exercise_catalog'),
     
     # Workout Function Urls
     path('workout/new/', WorkoutCreateView.as_view(), name='workout_create'),
     path('workout/<int:pk>/', WorkoutDetailView.as_view(), name='workout_detail'),
     path('history/', WorkoutHistoryView.as_view(), name='workout_history'),
     path('workout/<int:pk>/delete/', WorkoutDeleteView.as_view(), name='workout_delete'),
     path('workout/<int:pk>/edit/', DraftUpdateView.as_view(), name='workout_edit'),
     
     #Draft Function Urls
     path('drafts/<int:pk>/add-exercises/', DraftAddExercisesView.as_view(), name='draft_add_exercises'),
     path('drafts/', DraftListView.as_view(), name='draft_list'),
     path('drafts/<int:pk>/edit/', DraftUpdateView.as_view(), name='draft_edit'),
     path('drafts/<int:pk>/delete/', DraftDeleteView.as_view(), name='draft_delete'),
]