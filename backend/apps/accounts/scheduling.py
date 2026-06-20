"""Lesson-unlock schedule + streak/freeze-token engine (Phase 15).

New lessons unlock only on scheduled weekdays (default Mon/Wed/Fri); reviews are
available any day. A streak breaks only when a *scheduled* day is missed and no
freeze token is left — otherwise a freeze is auto-consumed. All knobs live in
settings (LESSON_UNLOCK_WEEKDAYS, STREAK_*).
"""

from __future__ import annotations

from datetime import date, timedelta

from django.conf import settings


def unlock_weekdays() -> set[int]:
    return set(settings.LESSON_UNLOCK_WEEKDAYS)


def is_unlock_day(d: date | None = None) -> bool:
    d = d or date.today()
    return d.weekday() in unlock_weekdays()


def next_unlock_date(d: date | None = None) -> date:
    d = d or date.today()
    for i in range(1, 8):
        nd = d + timedelta(days=i)
        if nd.weekday() in unlock_weekdays():
            return nd
    return d  # unreachable when at least one weekday is scheduled


def _missed_scheduled(last_active: date, today: date) -> int:
    """Scheduled days strictly between last_active and today (i.e. missed)."""
    count = 0
    d = last_active + timedelta(days=1)
    while d < today:
        if d.weekday() in unlock_weekdays():
            count += 1
        d += timedelta(days=1)
    return count


def register_activity(user, today: date | None = None):
    """Record that the user practiced today; update streak + freeze tokens.

    Best-effort: callers wrap this so a failure never breaks the core action.
    """
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
        missed = _missed_scheduled(rec.last_active_date, today)
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
    today = date.today()
    return {
        "current_streak": rec.current_streak if rec else 0,
        "longest_streak": rec.longest_streak if rec else 0,
        "freeze_tokens": (
            rec.freeze_tokens_available if rec else settings.STREAK_INITIAL_FREEZE_TOKENS
        ),
        "last_active_date": (
            rec.last_active_date.isoformat() if rec and rec.last_active_date else None
        ),
        "today_is_unlock_day": is_unlock_day(today),
        "next_unlock_date": next_unlock_date(today).isoformat(),
        "unlock_weekdays": sorted(unlock_weekdays()),
    }
