"""CEFR level helpers, and the one place the level rule is defined.

A user only sees content at or below their level. Lower levels are open for
review, their own level is the linear path, and higher levels are never shown.

This lives in `accounts` (which owns `CEFR_LEVELS`) so vocabulary, grammar,
history, videos and curriculum can all apply the rule without importing
`curriculum`.
"""

from .models import CEFR_LEVELS

# A1=0, A2=1, … C2=5. (Codes also happen to sort lexicographically, but rank
# explicitly rather than relying on that.)
LEVEL_RANK = {code: i for i, (code, _) in enumerate(CEFR_LEVELS)}
# Grundlagen, the optional starter units before A1. Content only: no user is at
# A0, so it ranks below every level and is always open, like review.
STARTER_LEVEL = "A0"
LEVEL_RANK[STARTER_LEVEL] = -1
LOWEST_LEVEL = CEFR_LEVELS[0][0]
# The course ends at B1 (owner, 2026-10-20): passing its exam finishes the
# course. B2-C2 stay in CEFR_LEVELS for the model choices only.
TOP_LEVEL = "B1"
COURSE_LEVELS = [code for code, _ in CEFR_LEVELS if LEVEL_RANK[code] <= LEVEL_RANK[TOP_LEVEL]]


def level_rank(code: str) -> int:
    return LEVEL_RANK.get(code, 0)


def cap_level(code: str) -> str:
    """A level within the course: anything above B1 becomes B1."""
    return code if level_rank(code) <= LEVEL_RANK[TOP_LEVEL] else TOP_LEVEL


def visible_levels(user_level: str) -> list[str]:
    """Every level at or below `user_level`, in order."""
    ceiling = level_rank(user_level)
    return [code for code, _ in CEFR_LEVELS if level_rank(code) <= ceiling]


def is_level_visible(user_level: str, content_level: str) -> bool:
    return level_rank(content_level) <= level_rank(user_level)


def visible_levels_for(user) -> list[str]:
    """Levels a request's user may browse.

    Guests have no level, so they only see the lowest one. Used by the pages
    guests can open (Word Bank, Grammar).
    """
    if not getattr(user, "is_authenticated", False):
        return visible_levels(LOWEST_LEVEL)
    profile = getattr(user, "profile", None)
    return visible_levels(profile.cefr_level if profile else LOWEST_LEVEL)
