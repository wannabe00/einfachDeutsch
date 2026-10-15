"""Applying one SM-2 review to a user's progress on a word.

Shared by the flashcard review endpoint and the checks (apps.curriculum.checks),
so a word answered in a check moves through spaced repetition exactly like a
flashcard rated with the same quality.
"""

from django.utils import timezone

from .models import ReviewLog, WordProgress
from .srs import calculate_next_review


def apply_review(progress: WordProgress, quality: int) -> WordProgress:
    """Update `progress` in memory for a review rated `quality` (0-5)."""
    reps, ease, interval, next_review = calculate_next_review(
        progress.repetitions, progress.ease_factor, progress.interval, quality
    )
    progress.repetitions = reps
    progress.ease_factor = ease
    progress.interval = interval
    progress.next_review = next_review
    progress.last_reviewed = timezone.now()
    progress.times_seen += 1
    if quality == 0:
        progress.times_wrong += 1
        progress.lapses += 1
    else:
        progress.times_correct += 1
    return progress


def record_review(user, word, quality: int) -> WordProgress:
    """Apply and save a review for a signed-in user, and log it."""
    progress, _ = WordProgress.objects.get_or_create(user=user, word=word)
    apply_review(progress, quality).save()
    ReviewLog.objects.create(word=word, quality=quality, user=user)
    return progress
