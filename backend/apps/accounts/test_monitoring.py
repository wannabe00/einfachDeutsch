"""The security log and the alert when an AI cap is hit."""

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIClient

from apps.ai_assistant.budget import BudgetExceeded, spend


class SecurityLogTests(TestCase):
    def setUp(self):
        cache.clear()
        get_user_model().objects.create_user("fred", password="pw-12345")

    def login(self, password):
        cache.clear()
        return APIClient().post("/api/auth/login/", {"username": "fred", "password": password})

    def test_sign_ins_are_logged_without_names(self):
        with self.assertLogs("security", "INFO") as logs:
            self.login("wrong")
            self.login("pw-12345")
        self.assertTrue(logs.output[0].startswith("WARNING:security:login_failed user=-"))
        self.assertRegex(logs.output[1], r"INFO:security:login user=\d+ ip=")
        self.assertNotIn("fred", " ".join(logs.output))

    def test_an_ai_cap_alerts_once_a_day(self):
        with self.settings(AI_DAILY_CAPS={"talk": 1}), self.assertLogs("security", "ERROR") as logs:
            spend("talk")
            for _ in range(3):
                with self.assertRaises(BudgetExceeded):
                    spend("talk")
        self.assertEqual(len(logs.output), 1)
        self.assertIn("ai_cap_reached feature=talk", logs.output[0])
