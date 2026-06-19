from django.db import models

from apps.books.models import Chapter


class Word(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="words")
    english = models.CharField(max_length=200)  # shown to the user: "dog"
    german = models.CharField(max_length=200)  # correct answer: "der Hund"
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["english"]

    def __str__(self):
        return f"{self.english} → {self.german}"


class WordProgress(models.Model):
    """SM-2 spaced-repetition state for a single word."""

    word = models.OneToOneField(Word, on_delete=models.CASCADE, related_name="progress")
    repetitions = models.IntegerField(default=0)
    ease_factor = models.FloatField(default=2.5)
    interval = models.IntegerField(default=1)  # days until next review
    next_review = models.DateField(auto_now_add=True)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    # Per-word performance tracking (updated on every review).
    times_seen = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    times_wrong = models.IntegerField(default=0)
    lapses = models.IntegerField(default=0)  # times rated "Again"

    def __str__(self):
        return f"{self.word.english} — next: {self.next_review}"


class ReviewLog(models.Model):
    """One row per review event — enables historical activity charts.

    WordProgress only keeps the *latest* review; this keeps the full history.
    """

    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="review_logs")
    quality = models.IntegerField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-reviewed_at"]

    def __str__(self):
        return f"{self.word.english} @ {self.reviewed_at:%Y-%m-%d} (q{self.quality})"
