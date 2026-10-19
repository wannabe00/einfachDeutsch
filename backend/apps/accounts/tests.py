"""The daily streak and two-factor login."""

import base64
import time
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from . import totp
from .scheduling import register_activity

MON = date(2026, 10, 19)


@override_settings(STREAK_INITIAL_FREEZE_TOKENS=1, STREAK_FREEZE_EARN_DAYS=0)
class DailyStreakTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("anna", password="pw")

    def day(self, n):
        return register_activity(self.user, MON + timedelta(days=n))

    def test_every_day_counts(self):
        for n in range(4):  # Mon-Thu, weekdays don't matter any more
            rec = self.day(n)
        self.assertEqual(rec.current_streak, 4)
        self.assertEqual(self.day(3).current_streak, 4)  # twice a day counts once

    def test_a_missed_day_uses_a_freeze_then_breaks(self):
        self.day(0)
        rec = self.day(2)  # missed day 1: the one freeze saves it
        self.assertEqual((rec.current_streak, rec.freeze_tokens_available), (2, 0))
        rec = self.day(4)  # missed day 3, no freeze left
        self.assertEqual(rec.current_streak, 1)
        self.assertEqual(rec.longest_streak, 2)


class TotpTests(TestCase):
    def test_rfc6238_reference_code(self):
        # RFC 6238 appendix B: SHA1 key "12345678901234567890", T=59s -> 94287082.
        secret = base64.b32encode(b"12345678901234567890").decode()
        self.assertEqual(totp.code_at(secret, 59 // 30, digits=8), "94287082")
        self.assertEqual(totp.matching_step(secret, "287082", now=59), 1)
        self.assertIsNone(totp.matching_step(secret, "000000", now=59))


class TwoFactorLoginTests(TestCase):
    def setUp(self):
        cache.clear()  # login throttle
        self.user = get_user_model().objects.create_user("anna", password="pw-12345")
        self.api = APIClient()
        self.api.force_authenticate(self.user)

    def login(self, **extra):
        cache.clear()  # the strict login throttle isn't under test here
        return APIClient().post(
            "/api/auth/login/", {"username": "anna", "password": "pw-12345", **extra}, format="json"
        )

    def now_code(self):
        secret = get_user_model().objects.get(pk=self.user.pk).profile.totp_secret
        return totp.code_at(secret, int(time.time() // totp.STEP))

    def turn_on(self):
        self.assertIn("otpauth://", self.api.post("/api/accounts/2fa/setup/").json()["uri"])
        self.first_code = self.now_code()
        res = self.api.post(
            "/api/accounts/2fa/enable/", {"code": self.first_code, "password": "pw-12345"}
        )
        self.assertEqual(res.status_code, 200)
        return res.json()["backup_codes"]

    def test_login_asks_for_the_code_after_the_password(self):
        self.assertEqual(self.login().status_code, 200)  # off: password is enough
        backup = self.turn_on()
        self.assertEqual(len(backup), 8)
        res = self.login()
        self.assertEqual(res.status_code, 400)
        self.assertIn("code", res.json())
        bad = APIClient().post("/api/auth/login/", {"username": "anna", "password": "x"})
        self.assertNotIn("code", bad.json())  # wrong password never reveals 2FA
        self.assertEqual(self.login(code="000000").status_code, 400)
        self.assertEqual(self.login(code=backup[0]).status_code, 200)
        self.assertEqual(self.login(code=backup[0]).status_code, 400)  # used up

    def test_a_code_works_once(self):
        self.turn_on()  # enabling used this code
        self.assertEqual(self.login(code=self.first_code).status_code, 400)

    def test_turning_off_needs_the_password(self):
        self.turn_on()
        self.assertEqual(self.api.post("/api/accounts/2fa/disable/", {}).status_code, 400)
        res = self.api.post("/api/accounts/2fa/disable/", {"password": "pw-12345"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.login().status_code, 200)
