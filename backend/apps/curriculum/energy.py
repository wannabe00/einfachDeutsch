"""Energy logic (Spec v3) — free-tier limiter on NEW path lessons.

Model: a bar of `ENERGY_MAX` (default 3). Each new lesson completion costs 1.
It regenerates +1 every `ENERGY_REFILL_HOURS` (default 4), capped at max. Values
are tunable via settings/env. Premium users have unlimited energy and bypass all
of this (`has_premium` short-circuits in the caller / helpers below).

`EnergyState.balance` stores the value as of `last_refill_at`; the live value is
computed here so we don't need a background job.
"""

from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import EnergyState

ENERGY_MAX = getattr(settings, "ENERGY_MAX", 3)
ENERGY_REFILL_HOURS = getattr(settings, "ENERGY_REFILL_HOURS", 4)


def _has_premium(user) -> bool:
    profile = getattr(user, "profile", None)
    return bool(profile and profile.has_premium)


def get_state(user) -> EnergyState:
    state, _ = EnergyState.objects.get_or_create(user=user)
    return state


def _regen_since(state: EnergyState, now) -> tuple[int, "timezone.datetime"]:
    """Returns (live_balance, new_last_refill_at) applying time-based regen,
    without saving. When already full, last_refill_at is pinned to `now`."""
    if state.balance >= ENERGY_MAX:
        return state.balance, now
    elapsed = now - state.last_refill_at
    gained = int(elapsed / timedelta(hours=ENERGY_REFILL_HOURS))
    if gained <= 0:
        return state.balance, state.last_refill_at
    new_balance = min(ENERGY_MAX, state.balance + gained)
    if new_balance >= ENERGY_MAX:
        return new_balance, now
    # Advance the clock by the whole refills consumed so the remainder carries.
    new_anchor = state.last_refill_at + timedelta(hours=ENERGY_REFILL_HOURS * gained)
    return new_balance, new_anchor


def current_energy(user) -> int:
    """Live energy for a user (premium → sentinel large number)."""
    if _has_premium(user):
        return ENERGY_MAX  # callers should check has_premium; kept sane otherwise
    state = get_state(user)
    balance, _ = _regen_since(state, timezone.now())
    return balance


def seconds_until_next(user) -> int | None:
    """Seconds until the next +1 refill, or None if full / premium."""
    if _has_premium(user):
        return None
    now = timezone.now()
    state = get_state(user)
    balance, anchor = _regen_since(state, now)
    if balance >= ENERGY_MAX:
        return None
    next_at = anchor + timedelta(hours=ENERGY_REFILL_HOURS)
    return max(0, int((next_at - now).total_seconds()))


def consume(user, amount: int = 1) -> bool:
    """Spend energy on lesson completion. Premium always succeeds. Returns
    False (and changes nothing) if a free user lacks energy."""
    if _has_premium(user):
        return True
    now = timezone.now()
    state = get_state(user)
    balance, anchor = _regen_since(state, now)
    if balance < amount:
        # Persist any regen we computed so the bar is accurate next read.
        state.balance, state.last_refill_at = balance, anchor
        state.save(update_fields=["balance", "last_refill_at"])
        return False
    # Spending from a full bar starts the refill clock now.
    state.last_refill_at = now if balance >= ENERGY_MAX else anchor
    state.balance = balance - amount
    state.save(update_fields=["balance", "last_refill_at"])
    return True
