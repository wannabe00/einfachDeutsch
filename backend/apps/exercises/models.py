from django.db import models

from apps.books.models import Chapter


class Exercise(models.Model):
    TYPE_CHOICES = [
        # Simple text-answer types (use correct_answer).
        ("translation", "Translate to German"),
        ("fill_blank", "Fill in the Blank"),
        ("article", "Choose Correct Article"),
        ("conjugation", "Conjugate the Verb"),
        ("free_text", "Free Text Answer"),
        # Interactive types (use payload).
        ("multiple_choice", "Multiple Choice"),
        ("matching", "Match Pairs"),
        ("sentence_order", "Put Words in Order"),
        ("word_bank", "Fill Blanks from a Word Bank"),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="exercises")
    exercise_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    prompt = models.TextField()
    correct_answer = models.TextField(blank=True)  # for simple types
    # Type-specific data + solution for interactive types. Shapes:
    #   multiple_choice: {"options": [...], "answer": "..."}
    #   matching:        {"pairs": [["links","rechts"], ...]}
    #   sentence_order:  {"tokens": [...], "answer": ["correct","order"]}
    #   word_bank:       {"text": "Ich ___ in ___.", "bank": [...],
    #                     "answers": ["wohne", "Berlin"]}
    payload = models.JSONField(default=dict, blank=True)
    hint = models.TextField(blank=True)
    explanation = models.TextField(blank=True)
    source = models.CharField(max_length=120, blank=True)  # e.g. book + page
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.exercise_type}] {self.prompt[:60]}"


class ExerciseAttempt(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="attempts")
    user_answer = models.TextField()
    is_correct = models.BooleanField()
    ai_feedback = models.TextField(blank=True)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-attempted_at"]

    def __str__(self):
        result = "correct" if self.is_correct else "incorrect"
        return f"Attempt #{self.pk} ({result})"
