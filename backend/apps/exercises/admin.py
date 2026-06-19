from django.contrib import admin

from .models import Exercise, ExerciseAttempt


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["prompt", "exercise_type", "chapter"]
    list_filter = ["chapter", "exercise_type"]
    search_fields = ["prompt", "correct_answer"]


@admin.register(ExerciseAttempt)
class ExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ["exercise", "user", "is_correct", "attempted_at"]
    list_filter = ["is_correct", "user"]
