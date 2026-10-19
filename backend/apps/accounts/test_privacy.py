"""Export my data is complete and secret-free; deleting an account deletes it all."""

import json
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.ai_assistant.models import Conversation, Message
from apps.vocabulary.models import SavedWord


class DataRightsTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_user(
            "gina", password="pw-12345", email="g@x.io"
        )
        self.api = APIClient()
        self.api.force_authenticate(self.user)
        SavedWord.objects.create(user=self.user, german="der Tisch", english="table")
        convo = Conversation.objects.create(user=self.user, title="Hallo")
        Message.objects.create(conversation=convo, role="user", content="Wie geht's?")
        Token.objects.create(user=self.user)
        profile = self.user.profile
        profile.totp_secret = "SECRETSECRET"
        profile.save()

    def test_export_has_everything_and_no_secrets(self):
        res = self.api.get("/api/accounts/export/")
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(body["account"]["email"], "g@x.io")
        data = body["data"]
        self.assertEqual(data["vocabulary.SavedWord"][0]["german"], "der Tisch")
        self.assertEqual(data["ai_assistant.Message"][0]["content"], "Wie geht's?")
        self.assertIn("accounts.UserProfile", data)
        dumped = json.dumps(body)
        for secret in ("SECRETSECRET", Token.objects.get(user=self.user).key, "pbkdf2"):
            self.assertNotIn(secret, dumped)
        self.assertNotIn("authtoken.Token", data)

    @override_settings(CLOUDINARY_CLOUD_NAME="demo")
    def test_deleting_the_account_removes_data_and_the_picture(self):
        self.user.profile.avatar_url = "https://res.cloudinary.com/demo/x.jpg"
        self.user.profile.save()
        user_id = self.user.id
        with mock.patch("cloudinary.uploader.destroy") as destroy:
            res = self.api.post("/api/accounts/delete/", {"password": "pw-12345"})
        self.assertEqual(res.status_code, 200)
        destroy.assert_called_once()
        self.assertEqual(destroy.call_args.args[0], f"einfachdeutsch/avatars/user_{user_id}")
        self.assertFalse(get_user_model().objects.filter(username="gina").exists())
        self.assertFalse(
            SavedWord.objects.exists() or Message.objects.exists() or Token.objects.exists()
        )
