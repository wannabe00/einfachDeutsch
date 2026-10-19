"""The daily streak and two-factor login."""

import base64
import time
from datetime import date, timedelta

from django.conf import settings
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


class SocialLoginTests(TestCase):
    """The Google/GitHub code exchange is wired to allauth's OAuth client (a
    library upgrade once broke it with a TypeError, i.e. a 500)."""

    def setUp(self):
        cache.clear()  # login throttle (the code exchange is throttled per IP)

    def test_a_bad_code_is_a_clean_400(self):
        from unittest import mock

        refused = mock.Mock(status_code=400, ok=False, headers={}, text="{}")
        refused.json.return_value = {"error": "bad_verification_code"}
        for provider in ("google", "github"):
            with mock.patch("requests.Session.request", return_value=refused):
                res = APIClient().post(f"/api/auth/{provider}/", {"code": "bogus"}, format="json")
            self.assertEqual(res.status_code, 400, provider)


class RateLimitTests(TestCase):
    """Password checks, client addresses behind the proxy, and the admin login."""

    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_user("carl", password="orig-pass-123")
        self.api = APIClient()
        self.api.force_authenticate(self.user)

    def test_password_change_needs_the_current_password(self):
        new = {"new_password1": "New-pass-4567", "new_password2": "New-pass-4567"}
        res = self.api.post("/api/auth/password/change/", {"old_password": "WRONG", **new})
        self.assertEqual(res.status_code, 400)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("orig-pass-123"))
        res = self.api.post("/api/auth/password/change/", {"old_password": "orig-pass-123", **new})
        self.assertEqual(res.status_code, 200)

    def test_password_checks_are_limited(self):
        codes = [
            self.api.post("/api/accounts/delete/", {"password": "guess"}).status_code
            for _ in range(6)
        ]
        self.assertEqual(codes[:5], [400] * 5)
        self.assertEqual(codes[5], 429)

    def test_a_faked_forwarded_for_does_not_dodge_the_login_limit(self):
        rf = {**settings.REST_FRAMEWORK, "NUM_PROXIES": 1}
        with self.settings(REST_FRAMEWORK=rf):
            codes = [
                APIClient(HTTP_X_FORWARDED_FOR=f"6.6.6.{i}, 203.0.113.7")
                .post("/api/auth/login/", {"username": "carl", "password": "x"})
                .status_code
                for i in range(6)
            ]
        self.assertEqual(codes[5], 429)

    def test_admin_login_is_limited(self):
        from django.test import Client

        c = Client()
        codes = [
            c.post("/admin/login/", {"username": "x", "password": "y"}).status_code
            for _ in range(6)
        ]
        self.assertEqual(codes[5], 429)

    def test_client_ip_check_is_staff_only(self):
        self.assertEqual(self.api.get("/api/accounts/client-ip/").status_code, 403)
        self.user.is_staff = True
        self.user.save()
        self.assertIn("throttle_ip", self.api.get("/api/accounts/client-ip/").json())


@override_settings(ADMIN_REQUIRE_2FA=True)
class AdminLoginTests(TestCase):
    """Staff need two-factor login for the admin, and the code is asked there."""

    def setUp(self):
        cache.clear()
        self.staff = get_user_model().objects.create_user("ada", password="pw-12345", is_staff=True)

    def login(self, **extra):
        from django.test import Client

        cache.clear()
        return Client().post("/admin/login/", {"username": "ada", "password": "pw-12345", **extra})

    def test_staff_without_2fa_are_refused(self):
        res = self.login()
        self.assertEqual(res.status_code, 200)  # the form again, with the error
        self.assertContains(res, "Turn on two-factor login")

    def test_the_code_is_checked(self):
        profile = self.staff.profile
        profile.totp_secret = totp.new_secret()
        profile.totp_enabled = True
        profile.save()
        self.assertContains(self.login(code="000000"), "current code")
        code = totp.code_at(profile.totp_secret, int(time.time() // totp.STEP))
        self.assertEqual(self.login(code=code).status_code, 302)  # into the admin

    def test_public_endpoints_stay_public_and_the_rest_need_a_login(self):
        guest = APIClient()
        for url in ("/api/books/", "/api/grammar/rules/", "/api/vocabulary/words/"):
            self.assertEqual(guest.get(url).status_code, 200, url)
        self.assertEqual(guest.get("/api/accounts/export/").status_code, 401)


class InputSafetyTests(TestCase):
    """The user endpoint can't be written, and avatars must be photos."""

    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_user("dora", password="pw", first_name="Dora")
        self.api = APIClient()
        self.api.force_authenticate(self.user)

    def test_auth_user_endpoint_changes_nothing(self):
        self.api.patch(
            "/api/auth/user/",
            {"is_staff": True, "username": "admin2", "first_name": "X"},
            format="json",
        )
        self.user.refresh_from_db()
        self.assertEqual(
            (self.user.is_staff, self.user.username, self.user.first_name), (False, "dora", "Dora")
        )

    @override_settings(CLOUDINARY_CLOUD_NAME="demo")
    def test_svg_avatars_are_refused(self):
        from unittest import mock

        from django.core.files.uploadedfile import SimpleUploadedFile

        svg = SimpleUploadedFile("x.svg", b"<svg onload=alert(1)/>", content_type="image/svg+xml")
        with mock.patch("cloudinary.uploader.upload") as upload:
            res = self.api.post("/api/accounts/avatar/", {"image": svg}, format="multipart")
        self.assertEqual(res.status_code, 400)
        upload.assert_not_called()
        jpg = SimpleUploadedFile("x.jpg", b"\xff\xd8\xff", content_type="image/jpeg")
        with mock.patch(
            "cloudinary.uploader.upload",
            return_value={"secure_url": "https://res.cloudinary.com/x.jpg"},
        ) as upload:
            res = self.api.post("/api/accounts/avatar/", {"image": jpg}, format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(upload.call_args.kwargs["format"], "jpg")
