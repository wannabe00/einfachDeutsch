"""CEFR level helpers — the single source of truth for the ≤-level rule.

Spec v3: a user only ever sees content **at or below their level**. Below = optional
review (fully open), current = the linear path, above = never shown at all.

This lives in `accounts` (which owns `CEFR_LEVELS`) so every app — vocabulary,
grammar, history, videos, curriculum — can gate without importing `curriculum`.
"""

from .models import CEFR_LEVELS

# A1=0, A2=1, … C2=5. (Codes also happen to sort lexicographically, but rank
# explicitly rather than relying on that.)
LEVEL_RANK = {code: i for i, (code, _) in enumerate(CEFR_LEVELS)}
LOWEST_LEVEL = CEFR_LEVELS[0][0]


def level_rank(code: str) -> int:
    return LEVEL_RANK.get(code, 0)


def visible_levels(user_level: str) -> list[str]:
    """Every level at or below `user_level`, in order."""
    ceiling = level_rank(user_level)
    return [code for code, _ in CEFR_LEVELS if level_rank(code) <= ceiling]


def is_level_visible(user_level: str, content_level: str) -> bool:
    return level_rank(content_level) <= level_rank(user_level)


def visible_levels_for(user) -> list[str]:
    """Levels a request's user may browse.

    Guests have no level, so they see only the lowest one — never forward
    content. Used by the guest-OK pages (Word Bank, Grammar).
    """
    if not getattr(user, "is_authenticated", False):
        return visible_levels(LOWEST_LEVEL)
    profile = getattr(user, "profile", None)
    return visible_levels(profile.cefr_level if profile else LOWEST_LEVEL)
