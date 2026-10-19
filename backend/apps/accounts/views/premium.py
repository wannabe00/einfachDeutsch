"""Premium status. Subscribing (with the one 7-day trial) goes through Stripe
Checkout in billing.py; the admin flag stays as a manual fallback."""

from django.conf import settings
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
        "has_subscription": bool(profile.stripe_customer_id),
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def premium_status(request):
    """What the upsell needs: am I premium, and can I still start a trial?"""
    return Response(_status_payload(request.user.profile))
