"""Site-wide daily caps on the paid AI services, on top of the per-user
throttles: whatever happens (a bug, a bot, many accounts), one day can only
use so much. Caps and the off switch come from settings (AI_DAILY_CAPS,
AI_DISABLED); a feature over its cap answers like a missing key (503)."""

from django.conf import settings
from django.db import IntegrityError
from django.db.models import F
from django.utils import timezone

from .models import AIUsage


class BudgetExceeded(Exception):
    pass


def spend(feature: str, amount: int = 1) -> None:
    """Count `amount` against today's cap for `feature`, or raise BudgetExceeded."""
    if feature in settings.AI_DISABLED:
        raise BudgetExceeded(feature)
    cap = settings.AI_DAILY_CAPS.get(feature)
    today = timezone.localdate()
    rows = AIUsage.objects.filter(feature=feature, day=today)
    if cap is not None:
        rows = rows.filter(amount__lte=cap - amount)
    # One UPDATE, so two processes can't both pass the check.
    if rows.update(amount=F("amount") + amount):
        return
    if AIUsage.objects.filter(feature=feature, day=today).exists():
        raise BudgetExceeded(feature)  # the row is there, so the cap was hit
    if cap is not None and amount > cap:
        raise BudgetExceeded(feature)
    try:
        AIUsage.objects.create(feature=feature, day=today, amount=amount)
    except IntegrityError:  # another process made today's row first
        spend(feature, amount)


def used_today() -> dict[str, int]:
    rows = AIUsage.objects.filter(day=timezone.localdate())
    return {r.feature: r.amount for r in rows}
