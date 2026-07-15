"""Premium tier endpoints (Phase 23.7).

Until Stripe lands (23.16) premium is granted by a manual admin flag or by the
one-time 7-day trial started here. Nothing takes payment yet, so this stays
deliberately small: report status, and let a user start their trial once.
"""

from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def _status_payload(profile) -> dict:
    return {
        "has_premium": profile.has_premium,
        "premium_until": profile.premium_until,
        "trial_started_at": profile.trial_started_at,
        "trial_available": profile.trial_started_at is None and not profile.has_premium,
        "trial_days": settings.PREMIUM_TRIAL_DAYS,
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def premium_status(request):
    """What the upsell needs: am I premium, and can I still start a trial?"""
    return Response(_status_payload(request.user.profile))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_trial(request):
    """Start the one-time 7-day premium trial.

    `trial_started_at` is the guard — once set it's never cleared, so a trial
    can't be farmed by restarting it.
    """
    profile = request.user.profile

    if profile.trial_started_at is not None:
        return Response(
            {"detail": "Your trial has already been used."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if profile.has_premium:
        return Response(
            {"detail": "You already have premium."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    now = timezone.now()
    profile.trial_started_at = now
    profile.premium_until = now + timedelta(days=settings.PREMIUM_TRIAL_DAYS)
    profile.save(update_fields=["trial_started_at", "premium_until"])
    return Response(_status_payload(profile))
