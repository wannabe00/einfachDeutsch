"""Stripe billing: Checkout, the portal and the webhook (Stripe itself is mocked)."""

import hashlib
import hmac
import json
import time
from types import SimpleNamespace
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.views import billing

SECRET = "whsec_test"
STRIPE = {
    "STRIPE_SECRET_KEY": "sk_test_x",
    "STRIPE_WEBHOOK_SECRET": SECRET,
    "STRIPE_PRICE_MONTHLY": "price_month",
    "STRIPE_PRICE_ANNUAL": "price_year",
}
LATER = int(time.time()) + 30 * 86400


def signed(payload: dict) -> tuple[str, str]:
    body = json.dumps(payload)
    t = int(time.time())
    sig = hmac.new(SECRET.encode(), f"{t}.{body}".encode(), hashlib.sha256).hexdigest()
    return body, f"t={t},v1={sig}"


def subscription(status="active", **extra) -> dict:
    return {
        "id": "sub_1",
        "customer": "cus_1",
        "status": status,
        "metadata": {},
        "items": {"data": [{"current_period_end": LATER}]},
        **extra,
    }


@override_settings(**STRIPE)
class BillingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("anna", "a@x.de", "pw")
        self.api = APIClient()
        self.api.force_authenticate(self.user)
        self.stripe = mock.MagicMock()
        self.stripe.v1.customers.create.return_value = SimpleNamespace(id="cus_1")
        self.stripe.v1.checkout.sessions.create.return_value = SimpleNamespace(url="https://pay")
        self.enterContext(mock.patch.object(billing, "_client", return_value=self.stripe))

    def profile(self):
        self.user.profile.refresh_from_db()
        return self.user.profile

    def hook(self, event_type, obj, sub=None):
        retrieved = mock.MagicMock()
        retrieved.to_dict.return_value = sub or obj
        self.stripe.v1.subscriptions.retrieve.return_value = retrieved
        body, sig = signed({"id": "evt_1", "type": event_type, "data": {"object": obj}})
        return self.api.post(
            "/api/billing/webhook/",
            body,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=sig,
        )

    def test_checkout_gives_the_first_subscription_the_trial(self):
        res = self.api.post("/api/billing/checkout/", {"plan": "annual"}, format="json")
        self.assertEqual(res.json(), {"url": "https://pay"})
        params = self.stripe.v1.checkout.sessions.create.call_args.kwargs["params"]
        self.assertEqual(params["line_items"], [{"price": "price_year", "quantity": 1}])
        self.assertEqual(params["customer"], "cus_1")
        self.assertEqual(params["subscription_data"]["trial_period_days"], 7)
        self.assertEqual(self.profile().stripe_customer_id, "cus_1")

        self.user.profile.trial_started_at = timezone.now()
        self.user.profile.save()
        self.api.post("/api/billing/checkout/", {"plan": "monthly"}, format="json")
        params = self.stripe.v1.checkout.sessions.create.call_args.kwargs["params"]
        self.assertNotIn("trial_period_days", params["subscription_data"])
        self.assertEqual(self.stripe.v1.customers.create.call_count, 1)  # customer reused
        self.assertNotIn("automatic_tax", params)

    @override_settings(STRIPE_AUTOMATIC_TAX=True)
    def test_checkout_turns_on_stripe_tax(self):
        self.api.post("/api/billing/checkout/", {"plan": "monthly"}, format="json")
        params = self.stripe.v1.checkout.sessions.create.call_args.kwargs["params"]
        self.assertEqual(params["automatic_tax"], {"enabled": True})
        self.assertEqual(params["customer_update"]["address"], "auto")

    def test_checkout_needs_a_plan_and_a_key(self):
        res = self.api.post("/api/billing/checkout/", {"plan": "weekly"}, format="json")
        self.assertEqual(res.status_code, 400)
        billing._client.return_value = None
        res = self.api.post("/api/billing/checkout/", {"plan": "monthly"}, format="json")
        self.assertEqual(res.status_code, 503)

    def test_portal_needs_a_customer(self):
        self.assertEqual(self.api.post("/api/billing/portal/").status_code, 400)

    def test_webhook_rejects_a_bad_signature(self):
        res = self.api.post(
            "/api/billing/webhook/",
            json.dumps({"type": "customer.subscription.updated"}),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="t=1,v1=nope",
        )
        self.assertEqual(res.status_code, 400)

    def test_subscription_sets_and_ends_premium(self):
        self.user.profile.stripe_customer_id = "cus_1"
        self.user.profile.save()
        sub = subscription("trialing", trial_start=int(time.time()))
        self.assertEqual(self.hook("customer.subscription.created", sub).status_code, 200)
        self.hook("customer.subscription.created", sub)  # a repeat changes nothing
        profile = self.profile()
        self.assertTrue(profile.has_premium)
        self.assertEqual(profile.premium_until.timestamp(), LATER)
        self.assertIsNotNone(profile.trial_started_at)
        self.assertEqual(profile.stripe_subscription_id, "sub_1")

        self.hook("customer.subscription.deleted", subscription("canceled"))
        self.assertFalse(self.profile().has_premium)

    def test_checkout_completed_reads_the_subscription_and_finds_the_user(self):
        sub = subscription(metadata={"user_id": str(self.user.id)})
        self.hook("checkout.session.completed", {"id": "cs_1", "subscription": "sub_1"}, sub)
        self.stripe.v1.subscriptions.retrieve.assert_called_with("sub_1")
        self.assertTrue(self.profile().has_premium)
        self.assertEqual(self.profile().stripe_customer_id, "cus_1")

    def test_manual_flag_survives_a_cancelled_subscription(self):
        self.user.profile.is_premium = True
        self.user.profile.stripe_customer_id = "cus_1"
        self.user.profile.save()
        self.hook("customer.subscription.deleted", subscription("canceled"))
        self.assertTrue(self.profile().has_premium)

    def test_other_events_are_ignored(self):
        self.assertEqual(self.hook("invoice.paid", {"id": "in_1"}).status_code, 200)
        self.stripe.v1.subscriptions.retrieve.assert_not_called()
