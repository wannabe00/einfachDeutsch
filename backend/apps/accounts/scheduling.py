"""Daily streak + freeze tokens.

Every day you practise (a lesson, a review, an exercise) counts. A missed day
uses up a freeze token automatically; with none left the streak starts again.
The settings are STREAK_*.
"""

from __future__ import annotations

from datetime import date

from django.conf import settings


def _missed_days(last_active: date, today: date) -> int:
    """Days strictly between last_active and today (i.e. missed)."""
    return max(0, (today - last_active).days - 1)


def register_activity(user, today: date | None = None):
    """Record that the user practiced today and update the streak and freeze
    tokens. Most callers want `record_activity`, which can't raise."""
    from .models import StreakRecord

    today = today or date.today()
    rec, _ = StreakRecord.objects.get_or_create(
        user=user,
        defaults={"freeze_tokens_available": settings.STREAK_INITIAL_FREEZE_TOKENS},
    )

    if rec.last_active_date == today:
        return rec  # already counted today

    if rec.last_active_date is None:
        rec.current_streak = 1
    else:
        missed = _missed_days(rec.last_active_date, today)
        broke = False
        while missed > 0:
            if rec.freeze_tokens_available > 0:
                rec.freeze_tokens_available -= 1
                missed -= 1
            else:
                broke = True
                break
        rec.current_streak = 1 if broke else rec.current_streak + 1

    earn = settings.STREAK_FREEZE_EARN_DAYS
    if earn > 0 and rec.current_streak % earn == 0:
        rec.freeze_tokens_available = min(
            rec.freeze_tokens_available + 1, settings.STREAK_FREEZE_MAX
        )

    rec.longest_streak = max(rec.longest_streak, rec.current_streak)
    rec.last_active_date = today
    rec.save()
    return rec


def streak_status(user) -> dict:
    from .models import StreakRecord

    rec = StreakRecord.objects.filter(user=user).first()
    return {
        "current_streak": rec.current_streak if rec else 0,
        "longest_streak": rec.longest_streak if rec else 0,
        "freeze_tokens": (
            rec.freeze_tokens_available if rec else settings.STREAK_INITIAL_FREEZE_TOKENS
        ),
        "last_active_date": (
            rec.last_active_date.isoformat() if rec and rec.last_active_date else None
        ),
    }


def record_activity(user):
    """`register_activity` for use inside request handlers: a streak problem
    must never break the review or exercise the user just did."""
    try:
        register_activity(user)
    except Exception:  # noqa: BLE001
        pass
