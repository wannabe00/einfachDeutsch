"""Premium gating (Phase 23.7, Spec v3).

Premium = **unlimited energy + AI Assistant + AI explanations + Recite**. Free
users get the full path (energy-limited) and every content page, so this gate is
deliberately narrow: it only guards features that cost the owner money (Gemini)
or are the paid-tier promise.

Until Stripe (23.16) premium is a manual admin flag — but always gate on
`profile.has_premium`, **never** on a hardcoded user list.
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
