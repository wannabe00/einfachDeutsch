from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class LoginThrottle(AnonRateThrottle):
    """Brute-force guard for credential/code exchanges (per-IP, unauthenticated).

    Applied to username/password login and the social-login code exchange —
    the global anon rate (120/min) is far too generous for password guessing.
    """

    scope = "login"


class OnboardingThrottle(UserRateThrottle):
    """Per-user cap on the one-shot onboarding endpoint (defence in depth on
    top of the profile_complete lock)."""

    scope = "onboarding"
