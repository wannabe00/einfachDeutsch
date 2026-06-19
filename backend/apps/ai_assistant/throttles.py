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
