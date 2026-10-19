"""Stripe billing: Checkout to subscribe, the Customer Portal to manage, and the
webhook that turns Stripe's subscription state into `premium_until`.

The webhook never trusts the event body for state: it re-reads the subscription
from Stripe, so repeated or out-of-order events all end in the same result.
"""

import datetime

import stripe
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import UserProfile

# Stripe statuses that still give access until the period ends.
LIVE = {"active", "trialing", "past_due"}
SUBSCRIPTION_EVENTS = {
    "checkout.session.completed",
    "customer.subscription.created",
    "customer.subscription.updated",
    "customer.subscription.deleted",
}


def _client() -> stripe.StripeClient | None:
    key = settings.STRIPE_SECRET_KEY
    return stripe.StripeClient(key) if key else None


def _unavailable() -> Response:
    return Response(
        {"detail": "Payments aren't available right now."},
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


def _customer(client: stripe.StripeClient, profile: UserProfile) -> str:
    if not profile.stripe_customer_id:
        user = profile.user
        customer = client.v1.customers.create(
            params={"email": user.email or None, "metadata": {"user_id": str(user.id)}}
        )
        profile.stripe_customer_id = customer.id
        profile.save(update_fields=["stripe_customer_id"])
    return profile.stripe_customer_id


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout(request):
    """Start Stripe Checkout for `plan` (monthly | annual); returns its URL.
    The first subscription of an account gets the trial (card required)."""
    prices = {"monthly": settings.STRIPE_PRICE_MONTHLY, "annual": settings.STRIPE_PRICE_ANNUAL}
    price = prices.get(request.data.get("plan"))
    if not price:
        return Response({"detail": "Pick the monthly or yearly plan."}, status=400)
    client = _client()
    if client is None:
        return _unavailable()
    profile = request.user.profile
    if profile.stripe_subscription_id and profile.has_premium:
        return Response({"detail": "You already have a subscription."}, status=400)

    subscription = {"metadata": {"user_id": str(request.user.id)}}
    if profile.trial_started_at is None:
        subscription["trial_period_days"] = settings.PREMIUM_TRIAL_DAYS
    try:
        session = client.v1.checkout.sessions.create(
            params={
                "mode": "subscription",
                "customer": _customer(client, profile),
                "line_items": [{"price": price, "quantity": 1}],
                "subscription_data": subscription,
                "client_reference_id": str(request.user.id),
                "success_url": f"{settings.FRONTEND_URL}/settings?billing=success",
                "cancel_url": f"{settings.FRONTEND_URL}/settings?billing=cancelled",
            }
        )
    except stripe.StripeError:
        return Response({"detail": "Couldn't reach Stripe. Try again."}, status=502)
    return Response({"url": session.url})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def portal(request):
    """Open the Stripe Customer Portal (cancel, change plan, card, invoices)."""
    client = _client()
    if client is None:
        return _unavailable()
    profile = request.user.profile
    if not profile.stripe_customer_id:
        return Response({"detail": "You don't have a subscription yet."}, status=400)
    try:
        session = client.v1.billing_portal.sessions.create(
            params={
                "customer": profile.stripe_customer_id,
                "return_url": f"{settings.FRONTEND_URL}/settings",
            }
        )
    except stripe.StripeError:
        return Response({"detail": "Couldn't reach Stripe. Try again."}, status=502)
    return Response({"url": session.url})


def _stamp(seconds) -> datetime.datetime | None:
    return datetime.datetime.fromtimestamp(seconds, tz=datetime.UTC) if seconds else None


def apply_subscription(sub: dict) -> None:
    """Copy one Stripe subscription (as a plain dict) onto its user's profile."""
    profile = UserProfile.objects.filter(stripe_customer_id=sub["customer"]).first()
    if profile is None:
        user_id = (sub.get("metadata") or {}).get("user_id")
        profile = UserProfile.objects.filter(user_id=user_id).first() if user_id else None
    if profile is None:
        return
    # Newer API versions keep the period on the items, older ones on the subscription.
    items = (sub.get("items") or {}).get("data") or [{}]
    period_end = items[0].get("current_period_end") or sub.get("current_period_end")
    profile.stripe_customer_id = sub["customer"]
    profile.stripe_subscription_id = sub["id"]
    if sub["status"] in LIVE:
        profile.premium_until = _stamp(period_end)
    elif profile.premium_until and profile.premium_until > timezone.now():
        profile.premium_until = timezone.now()  # cancelled, unpaid or expired: ends now
    if profile.trial_started_at is None and sub.get("trial_start"):
        profile.trial_started_at = _stamp(sub["trial_start"])
    profile.save(
        update_fields=[
            "stripe_customer_id",
            "stripe_subscription_id",
            "premium_until",
            "trial_started_at",
        ]
    )


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def webhook(request):
    """Stripe's events, signature-checked. Only the subscription ones matter."""
    client = _client()
    if client is None or not settings.STRIPE_WEBHOOK_SECRET:
        return _unavailable()
    try:
        event = stripe.Webhook.construct_event(
            request.body,
            request.headers.get("Stripe-Signature", ""),
            settings.STRIPE_WEBHOOK_SECRET,
        ).to_dict()
    except (ValueError, stripe.SignatureVerificationError):
        return Response({"detail": "Bad signature."}, status=400)
    if event["type"] not in SUBSCRIPTION_EVENTS:
        return Response({"ok": True})
    obj = event["data"]["object"]
    sub_id = obj.get("subscription") if event["type"] == "checkout.session.completed" else obj["id"]
    if not sub_id:
        return Response({"ok": True})
    try:
        apply_subscription(client.v1.subscriptions.retrieve(sub_id).to_dict())
    except stripe.StripeError:
        return Response({"detail": "Couldn't reach Stripe."}, status=502)  # Stripe retries
    return Response({"ok": True})
