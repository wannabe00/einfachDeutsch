"""Premium gating.

Premium means unlimited energy, the AI Assistant, AI explanations and Recite.
Free users get the whole path (limited by energy) and every content page, so
this only guards features that cost money to run (Gemini).

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
