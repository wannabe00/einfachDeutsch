"""Premium gating.

The premium matrix (owner, 2026-10-20; $2.99/mo or $29.99/yr):

  Free:    the path (energy-limited), level exams, Review, Exercises, Drills,
           Word Bank, Grammar, Books, Videos, History lessons
  Premium: unlimited energy; the four skills — Lesen, Hören, Schreiben (incl. AI
           grading) and Sprechen / Talk to AI (TALK_MONTHLY_CAP: 5 talks of 5 min a month);
           AI Assistant (chat, mic, read-aloud); AI explanations; AI history lessons

Until payments exist, premium is a flag set in the admin. Always check
`profile.has_premium`, never a hardcoded list of users.
"""

from rest_framework.permissions import BasePermission


class IsPremium(BasePermission):
    """Allow only users with active premium (paid, trial, or admin flag).

    Denials carry `code="premium_required"` so the frontend can show the upsell
    instead of a generic error.
    """

    message = "Premium required."
    code = "premium_required"

    def has_permission(self, request, view) -> bool:
        user = request.user
        if not (user and user.is_authenticated):
            return False
        profile = getattr(user, "profile", None)
        return bool(profile and profile.has_premium)
