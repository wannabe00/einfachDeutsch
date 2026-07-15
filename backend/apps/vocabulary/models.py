from django.conf import settings
from django.db import models

from apps.books.models import Chapter

from .pos import PART_OF_SPEECH_CHOICES, guess_part_of_speech


class Word(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="words")
    english = models.CharField(max_length=200)  # shown to the user: "dog"
    german = models.CharField(max_length=200)  # correct answer: "der Hund"
    notes = models.TextField(blank=True)
    # The Word Bank groups by Level → part of speech (Phase 23.9). Left blank it
    # is guessed from the German on save; an explicit value always wins, so
    # curated content and admin corrections stick.
    part_of_speech = models.CharField(max_length=16, choices=PART_OF_SPEECH_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["english"]

    def save(self, *args, **kwargs):
        if not self.part_of_speech:
            self.part_of_speech = guess_part_of_speech(self.german)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.english} → {self.german}"


class WordProgress(models.Model):
    """SM-2 spaced-repetition state for one (user, word) pair.

    Progress is **per-user**; the Word itself is shared/global content. A row is
    created on demand the first time a signed-in user reviews a word. Guests get
    no persisted progress (the review endpoint computes but does not save).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="word_progress",
        null=True,
        blank=True,
    )
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="progress_records")
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

    class Meta:
        # One progress row per user per word.
        unique_together = [("user", "word")]

    def __str__(self):
        return f"{self.word.english} — next: {self.next_review}"


class ReviewLog(models.Model):
    """One row per review event — enables historical activity charts.

    WordProgress only keeps the *latest* review; this keeps the full history.
    Per-user (nullable for safety; the review endpoint always sets it).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_logs",
        null=True,
        blank=True,
    )
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="review_logs")
    quality = models.IntegerField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-reviewed_at"]

    def __str__(self):
        return f"{self.word.english} @ {self.reviewed_at:%Y-%m-%d} (q{self.quality})"
