"""Password reset: e-mail with a link to the app, then a new password."""

import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

RESET = "/api/auth/password/reset/"
CONFIRM = "/api/auth/password/reset/confirm/"


@override_settings(FRONTEND_URL="https://app.example")
class PasswordResetTests(TestCase):
    def setUp(self):
        cache.clear()  # throttle counters
        self.user = get_user_model().objects.create_user(
            "anna", email="anna@example.com", password="old-pass-123"
        )
        self.api = APIClient()

    def reset_link(self):
        self.assertEqual(self.api.post(RESET, {"email": "anna@example.com"}).status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        body = mail.outbox[0].body
        self.assertIn("anna", body)  # the username reminder
        uid, token = re.search(
            r"https://app\.example/reset-password/([^/\s]+)/(\S+)", body
        ).groups()
        return uid, token

    def test_reset_sets_a_new_password_and_signs_out_everywhere(self):
        old_token = Token.objects.create(user=self.user)
        uid, token = self.reset_link()
        res = self.api.post(
            CONFIRM,
            {
                "uid": uid,
                "token": token,
                "new_password1": "New-pass-456!",
                "new_password2": "New-pass-456!",
            },
        )
        self.assertEqual(res.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("New-pass-456!"))
        self.assertFalse(Token.objects.filter(key=old_token.key).exists())
        # The link works only once.
        again = self.api.post(
            CONFIRM,
            {
                "uid": uid,
                "token": token,
                "new_password1": "Other-pass-789!",
                "new_password2": "Other-pass-789!",
            },
        )
        self.assertEqual(again.status_code, 400)

    def test_unknown_email_looks_the_same_and_sends_nothing(self):
        res = self.api.post(RESET, {"email": "nobody@example.com"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_bad_token_and_weak_password_are_refused(self):
        uid, token = self.reset_link()
        bad = self.api.post(
            CONFIRM,
            {
                "uid": uid,
                "token": "wrong",
                "new_password1": "New-pass-456!",
                "new_password2": "New-pass-456!",
            },
        )
        self.assertEqual(bad.status_code, 400)
        weak = self.api.post(
            CONFIRM, {"uid": uid, "token": token, "new_password1": "123", "new_password2": "123"}
        )
        self.assertEqual(weak.status_code, 400)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("old-pass-123"))

    def test_reset_emails_are_rate_limited(self):
        codes = [self.api.post(RESET, {"email": "x@example.com"}).status_code for _ in range(6)]
        self.assertEqual(codes[-1], 429)

    def test_mail_server_failure_is_a_clear_503(self):
        from unittest import mock

        with mock.patch(
            "django.core.mail.backends.locmem.EmailBackend.send_messages",
            side_effect=OSError("blocked"),
        ):
            res = self.api.post(RESET, {"email": "anna@example.com"})
        self.assertEqual(res.status_code, 503)
        self.assertIn("couldn't send", res.json()["detail"])
