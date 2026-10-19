"""Per-user rate limits for the (Gemini-backed) AI endpoints.

AI calls cost the owner's limited free quota, so they get tighter caps than the
global defaults: a short burst limit plus a daily ceiling. Rates are configured
in settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] (env-overridable).
"""

from rest_framework.throttling import UserRateThrottle


class AIBurstThrottle(UserRateThrottle):
    scope = "ai_burst"


class AIDailyThrottle(UserRateThrottle):
    scope = "ai_daily"


class PlacementThrottle(UserRateThrottle):
    """Submitting the placement test asks Gemini for the level, and any account
    can take it, so submissions get their own small daily limit (loading the
    test is free)."""

    scope = "placement"

    def allow_request(self, request, view):
        return request.method != "POST" or super().allow_request(request, view)
