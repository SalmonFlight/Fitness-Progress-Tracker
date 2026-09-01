from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.db.models import Sum
from .models import Exercise, Set, Workout, PersonalRecord
from .forms import WorkoutForm
from users.models import Profile, WeightEntry

def get_draft_snapshot(draft):
    """Helper function to create a JSON-safe snapshot of draft sets."""
    
    snapshot = []
    #Creates a snapshot of the drafts current set
    #Used to revert to original state if the user cancels
    for set_obj in draft.sets.all().order_by('order'):
        snapshot.append({
            'id': set_obj.id,
            'exercise_id': set_obj.exercise_id,
            'set_count': set_obj.set_count,
            'reps': set_obj.reps,
            'weight': float(set_obj.weight) if set_obj.weight is not None else 0.0,
            'order': set_obj.order,
        })
    return snapshot

# ==================== HOMEPAGE ====================
class HomePageView(LoginRequiredMixin, ListView):
    """Displays the dashboard with various (refer to get_context_data function)"""
    model = Workout
    template_name = 'fitnessapp/home.html'
    context_object_name = 'workouts'
    
    def get_queryset(self):
        """Returns only workouts with the completed status"""
        return Workout.objects.filter(user=self.request.user, status='completed')
    
    def get(self, request, *args, **kwargs):
        """Clears session from previous workout creation attempts"""
        request.session.pop('selected_exercises', None)
        request.session.pop('saved_workout_data', None)
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        Retrieves all the information that will be displayed in the homepage:
        Username, weight stats, workout frequency/time, latest workout, and personal records.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Retrieves profile information to display on homepage
        profile, _ = Profile.objects.get_or_create(user=user) # Get or create user profile
        context['profile'] = profile
        context['current_weight'] = profile.current_weight
        context['goal_weight'] = profile.goal_weight
        
        # Retrieves Workout frequency and time information to display on homepage
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0)
        monthly = Workout.objects.filter(user=user, status='completed', date__gte=month_start)
        context['monthly_workout_count'] = monthly.count()
        context['monthly_hours'] = monthly.aggregate(total=Sum('duration'))['total'] or 0
        
        # Retrieves the Latest workout
        context['latest_workout'] = Workout.objects.filter(user=user, status='completed').order_by('-date').first()
        
        # Retrieves Personal Record Information
        tracked = profile.tracked_pr_exercises
        context['personal_records'] = PersonalRecord.objects.filter(
            user=user, exercise__name__in=tracked
        ).order_by('-weight')[:5] if tracked else []
        
        return context
        
# ==================== EXERCISE CATALOG ====================
class ExerciseCatalogView(LoginRequiredMixin, ListView):
    """
    Displays all exercises that exist in the database for users to choose from.
    Handles both:
    New Workouts (stores selection in session) and Draft Editing (syncs selection with draft)
    """
    model = Exercise
    template_name = 'fitnessapp/exercise_catalog.html'
    context_object_name = 'exercises'
    
    
    def get_queryset(self):
        """Returns all exercises in the database and sort by their names(alphabet)"""
        return Exercise.objects.all().order_by('name')
    
    def get_context_data(self, **kwargs):
        """
        Adds extra data to the template context:
        - All exercise categories 
        - Pre-selected exercises (from session or from draft)
        - Draft ID if editing a draft
        - A snapshot of the draft (to revert if user cancels)
        """
        context = super().get_context_data(**kwargs)
        
        # Pass all category choices to template for filtering
        context['categories'] = Exercise.CATEGORY_CHOICES
        
        # Check if we're coming from a draft edit page
        draft_id = self.request.GET.get('draft')
        if draft_id:
            # Get the draft and verify it belongs to the current user
            draft = get_object_or_404(Workout, id=draft_id, user=self.request.user, status='draft')
           
            # Create JSON-serializable snapshot if missing
            if 'draft_snapshot' not in self.request.session:
                self.request.session['draft_snapshot'] = get_draft_snapshot(draft)
            
            #Pre-select exercises already in the draft
            context['selected_exercises'] = draft.sets.all().values_list('exercise_id', flat=True)
            context['is_draft'] = True
            context['draft_id'] = draft_id
        else:
            # New workout — use session to remember selected exercises
            context['selected_exercises'] = self.request.session.get('selected_exercises', [])
            context['is_draft'] = False
        
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles form submission when user clicks "Continue".
        - For drafts: Syncs selected exercises with the draft (adds/removes)
        - For new workouts: Stores selected exercises in session for the next step
        """
        # Get list of selected exercise IDs from the form   
        selected_ids = [int(id) for id in request.POST.getlist('exercises')]
        
        # Check if coming from a draft (hidden field or URL parameter)
        draft_id = request.POST.get('draft_id') or request.GET.get('draft')
        
        if draft_id:
            # Get the draft
            draft = get_object_or_404(Workout, id=draft_id, user=request.user, status='draft')
            
            # Save snapshot before modifying
            if 'draft_snapshot' not in request.session:
                request.session['draft_snapshot'] = get_draft_snapshot(draft)
            
            #Gets id of exercises currently in the draft
            existing_ids = list(draft.sets.all().values_list('exercise_id', flat=True))
            
            # Remove unchecked exercises
            draft.sets.exclude(exercise_id__in=selected_ids).delete()
            
            # Add newly checked exercises
            for ex_id in selected_ids:
                if ex_id not in existing_ids:
                    Set.objects.create(
                        workout=draft,
                        exercise_id=ex_id,
                        set_count=0,
                        reps=0,
                        weight=0,
                        order=draft.sets.count()
                    )
            
            return redirect('draft_edit', pk=draft_id)
        else:
            #─── NEW WORKOUT MODE ───
            # Store selected exercises in session for the workout creation form
            request.session['selected_exercises'] = selected_ids
            request.session.save()
            
            return redirect('workout_create')

# ==================== WORKOUT FUNCTIONS ====================
class WorkoutCreateView(LoginRequiredMixin, CreateView):
    """
    Handles creating a new workout from scratch.
    Users select exercises from the catalog, then come here to fill in:
    - Workout name, date, duration, notes
    - Sets, reps, and weight for each selected exercise
    They can either save as a draft or complete the workout immediately.
    """
    model = Workout
    form_class = WorkoutForm
    template_name = 'fitnessapp/workout_form.html'
    
    def get(self, request, *args, **kwargs):
        """
        If the user clicks "Cancel" with ?clear=1 in the URL,
        clear any leftover session data from previous attempts.
        This prevents old exercises or form data from persisting.
        """
        if request.GET.get('clear'):
            request.session.pop('selected_exercises', None)
            request.session.pop('saved_workout_data', None)
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        Passes data to the template:
        - selected_exercises: The exercises the user picked in the catalog
        - saved: Any previously saved form data (so it persists if user goes back and forth)
        """
        context = super().get_context_data(**kwargs)
        selected_ids = self.request.session.get('selected_exercises', [])
        context['selected_exercises'] = Exercise.objects.filter(id__in=selected_ids)
        context['saved'] = self.request.session.get('saved_workout_data', {})
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handles form submissions.
        If the user clicks "Add Exercises", save all current form data to session
        and redirect to the exercise catalog so they can pick more.
        Otherwise, proceed with normal form validation.
        """
        if 'add_exercises' in request.POST:
            # Save everything the user has typed so far
            request.session['saved_workout_data'] = {
                'name': request.POST.get('name', ''),
                'date': request.POST.get('date', ''),
                'duration': request.POST.get('duration', ''),
                'notes': request.POST.get('notes', ''),
                'set_count': request.POST.getlist('set_count[]'),
                'reps': request.POST.getlist('reps[]'),
                'weight': request.POST.getlist('weight[]'),
            }
            request.session.save()
            return redirect('exercise_catalog')
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        Called when the form is valid.
        Creates the workout, saves it as draft or completed,
        creates the set entries for each exercise,
        and detects personal records if completed.
        """
        # Clear saved form data from session (no longer needed)
        self.request.session.pop('saved_workout_data', None)
        
        # Create the workout but don't save to DB yet
        workout = form.save(commit=False)
        workout.user = self.request.user
        workout.status = 'draft'
        
        # If the "Save Workout" button was clicked, mark as completed
        if 'save_workout' in self.request.POST:
            workout.status = 'completed'
        
        workout.save()
        
        # Get selected exercises from session and remove them
        selected_ids = self.request.session.pop('selected_exercises', [])
        exercises = Exercise.objects.filter(id__in=selected_ids)
        
        # Get sets, reps, and weights from the form
        set_counts = self.request.POST.getlist('set_count[]')
        reps = self.request.POST.getlist('reps[]')
        weights = self.request.POST.getlist('weight[]')
        
        # Create a Set entry for each exercise
        for i, exercise in enumerate(exercises):
            if i < len(set_counts) and set_counts[i]:
                Set.objects.create(
                    workout=workout,
                    exercise=exercise,
                    set_count=set_counts[i],
                    reps=reps[i],
                    weight=weights[i],
                    order=i  # Keep the order the user selected
                )
        
        # If completed, check for personal records and redirect to detail page
        if workout.status == 'completed':
            self.detect_prs(workout)
            messages.success(self.request, 'Workout saved! 🎉')
            return redirect('workout_detail', pk=workout.pk)
        
        # Otherwise, it's a draft — redirect to draft list
        messages.info(self.request, 'Draft saved.')
        return redirect('draft_list')
    
    def detect_prs(self, workout):
        """
        Checks each set in the workout against the user's existing personal records.
        If a set has a higher weight than the previous best, create a new PR entry.
        """
        for set_obj in workout.sets.all():
            # Get the user's previous best for this exercise
            previous = PersonalRecord.objects.filter(
                user=workout.user,
                exercise=set_obj.exercise
            ).order_by('-weight').first()
            
            # If no PR exists, or this set is heavier, create a new PR
            if not previous or set_obj.weight > previous.weight:
                PersonalRecord.objects.create(
                    user=workout.user,
                    exercise=set_obj.exercise,
                    workout=workout,  # Link the PR to this workout
                    weight=set_obj.weight,
                    reps=set_obj.reps,
                    date=workout.date.date()
                )

class WorkoutDetailView(LoginRequiredMixin, DetailView):
    """Displays all the workout details"""
    model = Workout
    template_name = 'fitnessapp/workout_detail.html'
    context_object_name = 'workout'
    
    def get_queryset(self):
        "Returns all Workout objects created by user"
        return Workout.objects.filter(user=self.request.user)

class WorkoutHistoryView(LoginRequiredMixin, ListView):
    """Displays all workouts logged as completed"""
    model = Workout
    template_name = 'fitnessapp/workout_history.html'
    context_object_name = 'workouts'
    paginate_by = 10
    
    def get_queryset(self):
        """Retrieves all workouts that the is completed(not saved as a draft)"""
        return Workout.objects.filter(
            user=self.request.user,
            status='completed'
        ).order_by('-date')

class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    """Deletes workout and things linked to the workout"""
    model = Workout
    template_name = 'fitnessapp/workout_confirm_delete.html'
    success_url = reverse_lazy('workout_history')
    
    def get_queryset(self):
        """Returns workouts that are already completed(drafts cant be deleted using this)"""
        return Workout.objects.filter(user=self.request.user, status='completed')
    
    def delete(self, request, *args, **kwargs):
        """Deletes the workout and removes any personal records that came from this workout."""
        workout = self.get_object()
        
        # Delete only PRs linked to this specific workout
        PersonalRecord.objects.filter(workout=workout).delete()
        
        messages.success(request, 'Workout and associated PRs deleted successfully.')
        return super().delete(request, *args, **kwargs)

# ==================== DRAFT FUNCTIONS ====================
class DraftListView(LoginRequiredMixin, ListView):
    """Displays all the workouts saved as drafts"""
    model = Workout
    template_name = 'fitnessapp/draft_list.html'
    context_object_name = 'drafts'
    
    def get_queryset(self):
        """Returns all workouts saved as drafts"""
        return Workout.objects.filter(user=self.request.user, status='draft')
    
    def get(self, request, *args, **kwargs):
        """
        Clears temporary session data (snapshot, selected exercises) 
        when user returns to draft list.
        """
        request.session.pop('draft_snapshot', None)
        request.session.pop('selected_exercises', None)
        return super().get(request, *args, **kwargs)
    
class DraftUpdateView(LoginRequiredMixin, UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'fitnessapp/draft_form.html'
    success_url = reverse_lazy('draft_list')
    
    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user, status='draft')

    def get(self, request, *args, **kwargs):
        draft = self.get_object()
        if 'draft_snapshot' not in request.session:
            request.session['draft_snapshot'] = get_draft_snapshot(draft)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = self.get_object()
        context['existing_sets'] = workout.sets.all().order_by('order')
        context['workout'] = workout
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            workout = self.get_object()
            snapshot = request.session.pop('draft_snapshot', None)
            
            if snapshot is not None:
                # Revert sets to exact initial snapshot state
                workout.sets.all().delete()
                for item in snapshot:
                    Set.objects.create(
                        workout=workout,
                        exercise_id=item['exercise_id'],
                        set_count=item['set_count'],
                        reps=item['reps'],
                        weight=item['weight'],
                        order=item['order']
                    )
            
            request.session.pop('selected_exercises', None)
            messages.info(request, "Changes canceled and draft restored to original state.")
            return redirect('draft_list')

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        workout = form.save()
        
        set_ids = self.request.POST.getlist('set_id[]')
        set_counts = self.request.POST.getlist('set_count[]')
        reps = self.request.POST.getlist('reps[]')
        weights = self.request.POST.getlist('weight[]')
        
        for i, set_id in enumerate(set_ids):
            if set_id:
                Set.objects.filter(id=set_id, workout=workout).update(
                    set_count=set_counts[i] if i < len(set_counts) else 0,
                    reps=reps[i] if i < len(reps) else 0,
                    weight=weights[i] if i < len(weights) else 0
                )
        
        self.request.session.pop('draft_snapshot', None)
        self.request.session.pop('selected_exercises', None)
        
        if 'save_workout' in self.request.POST:
            workout.status = 'completed'
            workout.save()
            self.detect_prs(workout)
            messages.success(self.request, 'Workout completed! 🎉')
            return redirect('workout_detail', pk=workout.pk)
        
        messages.success(self.request, 'Draft updated.')
        return redirect('draft_list')

    def detect_prs(self, workout):
        for set_obj in workout.sets.all():
            previous = PersonalRecord.objects.filter(
                user=workout.user,
                exercise=set_obj.exercise
            ).order_by('-weight').first()
            if not previous or set_obj.weight > previous.weight:
                PersonalRecord.objects.create(
                    user=workout.user,
                    exercise=set_obj.exercise,
                    workout=workout,  # <- ADD THIS
                    weight=set_obj.weight,
                    reps=set_obj.reps,
                    date=workout.date.date()
                )
    
class DraftAddExercisesView(LoginRequiredMixin, ListView):
    """The exercise catalog but this time for drafts only (still uses the same template)"""
    model = Exercise
    template_name = 'fitnessapp/exercise_catalog.html'
    context_object_name = 'exercises'
    
    def get_queryset(self):
        """Gets all exercises"""
        return Exercise.objects.all().order_by('name')
    
    def get_context_data(self, **kwargs):
        """
        Adds draft-specific context:
        - Pre-selects exercises already in the draft
        - Passes draft ID to template
        """
        context = super().get_context_data(**kwargs)
        draft_id = self.kwargs.get('pk')
        draft = Workout.objects.get(id=draft_id, user=self.request.user, status='draft')
        existing_ids = draft.sets.all().values_list('exercise_id', flat=True)
        context['selected_exercises'] = list(existing_ids)
        context['categories'] = Exercise.CATEGORY_CHOICES
        context['is_draft'] = True
        context['draft_id'] = draft_id
        return context
    
    def post(self, request, *args, **kwargs):
        """Saves selected exercises to session and redirects back to draft edit."""
        draft_id = kwargs.get('pk')
        selected_ids = request.POST.getlist('exercises')
        request.session['selected_exercises'] = [int(id) for id in selected_ids]
        request.session.save()
        return redirect('draft_edit', pk=draft_id)

class DraftDeleteView(LoginRequiredMixin, DeleteView):
    """Deletes a draft workout"""
    model = Workout
    template_name = 'fitnessapp/draft_confirm_delete.html'
    success_url = reverse_lazy('draft_list')
    
    def get_queryset(self):
        """returns all draft workouts"""
        return Workout.objects.filter(user=self.request.user, status='draft')
    
    def delete(self, request, *args, **kwargs):
        """Returns success message afer a drfat is deleted"""
        messages.success(request, 'Draft deleted successfully.')
        return super().delete(request, *args, **kwargs)