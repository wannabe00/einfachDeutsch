"""The starting level is chosen once; after that there is no free skipping."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class SetLevelTests(TestCase):
    def test_level_can_only_be_set_once(self):
        user = get_user_model().objects.create_user("anna", password="pw")
        api = APIClient()
        api.force_authenticate(user)

        first = api.post("/api/accounts/set-level/", {"cefr_level": "A2"}, format="json")
        self.assertEqual(first.status_code, 200)

        again = api.post("/api/accounts/set-level/", {"cefr_level": "C1"}, format="json")
        self.assertEqual(again.status_code, 403)
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.cefr_level, "A2")
