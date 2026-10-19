"""The AI Assistant's mic (speech to text) and speaker button (text to speech)."""

from unittest import mock

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from . import llm, views


class VoiceTests(TestCase):
    def setUp(self):
        cache.clear()  # AI throttle counters
        self.user = get_user_model().objects.create_user("anna", password="pw")
        self.user.profile.is_premium = True
        self.user.profile.save()
        self.api = APIClient()
        self.api.force_authenticate(self.user)

    def _audio(self, data=b"opus", kind="audio/webm;codecs=opus"):
        return {"audio": SimpleUploadedFile("voice.webm", data, content_type=kind)}

    def test_transcribe(self):
        with mock.patch.object(llm, "transcribe", return_value="Ich heiße Anna.") as tr:
            res = self.api.post("/api/ai/transcribe/", self._audio(), format="multipart")
        self.assertEqual(res.json(), {"content": "Ich heiße Anna."})
        tr.assert_called_once_with(b"opus", "audio/webm")  # codec part dropped

    def test_transcribe_rejects_bad_uploads(self):
        self.assertEqual(self.api.post("/api/ai/transcribe/", {}).status_code, 400)
        big = self._audio(b"x" * (views.MAX_AUDIO_BYTES + 1))
        self.assertEqual(self.api.post("/api/ai/transcribe/", big).status_code, 400)
        text = self._audio(kind="text/plain")
        self.assertEqual(self.api.post("/api/ai/transcribe/", text).status_code, 400)
        with mock.patch.object(llm, "transcribe", side_effect=llm.AIResponseError("x")):
            self.assertEqual(self.api.post("/api/ai/transcribe/", self._audio()).status_code, 502)

    def test_read_aloud(self):
        with mock.patch.object(llm, "read_aloud", return_value=b"mp3") as speak:
            res = self.api.post("/api/ai/read-aloud/", {"text": "der Tisch"}, format="json")
        self.assertEqual(
            (res.status_code, res["Content-Type"], res.content), (200, "audio/mpeg", b"mp3")
        )
        speak.assert_called_once_with("der Tisch")
        self.assertEqual(self.api.post("/api/ai/read-aloud/", {"text": " "}).status_code, 400)
        with mock.patch.object(llm, "read_aloud", side_effect=llm.AIConfigError("no key")):
            res = self.api.post("/api/ai/read-aloud/", {"text": "Hallo"}, format="json")
        self.assertEqual(res.status_code, 503)

    def test_read_aloud_ssml_is_escaped(self):
        ok = mock.Mock(status_code=200, content=b"mp3")
        with (
            self.settings(AZURE_SPEECH_KEY="k", AZURE_SPEECH_REGION="westeurope"),
            mock.patch.object(llm.httpx, "post", return_value=ok) as post,
        ):
            llm.read_aloud("a < b & </voice>")
        ssml = post.call_args.kwargs["content"].decode()
        self.assertIn("a &lt; b &amp; &lt;/voice&gt;", ssml)
        self.assertIn("mp3", post.call_args.kwargs["headers"]["X-Microsoft-OutputFormat"])

    def test_premium_only(self):
        self.user.profile.is_premium = False
        self.user.profile.save()
        self.assertEqual(self.api.post("/api/ai/transcribe/", self._audio()).status_code, 403)
        self.assertEqual(self.api.post("/api/ai/read-aloud/", {"text": "x"}).status_code, 403)


class CostGuardTests(TestCase):
    """Site-wide daily caps, off switches and size limits on the paid AI calls."""

    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_user("bob", password="pw")
        self.user.profile.is_premium = True
        self.user.profile.save()
        self.api = APIClient()
        self.api.force_authenticate(self.user)

    def test_spend_stops_at_the_cap(self):
        from .budget import BudgetExceeded, spend, used_today

        with self.settings(AI_DAILY_CAPS={"speech": 10}):
            spend("speech", 6)
            spend("speech", 4)  # exactly the cap is fine
            with self.assertRaises(BudgetExceeded):
                spend("speech", 1)
            with self.assertRaises(BudgetExceeded):
                spend("speech", 11)
        self.assertEqual(used_today()["speech"], 10)

    def test_a_feature_can_be_switched_off(self):
        from .budget import BudgetExceeded, spend

        with self.settings(AI_DISABLED={"talk"}), self.assertRaises(BudgetExceeded):
            spend("talk")

    def test_over_the_cap_the_provider_is_never_called(self):
        with (
            self.settings(AI_DAILY_CAPS={"speech": 5}),
            mock.patch.object(llm, "_azure", return_value=b"mp3") as azure,
        ):
            self.assertEqual(llm.read_aloud("Hallo"), b"mp3")
            with self.assertRaises(llm.AIBudgetError):
                llm.read_aloud("Hallo")
        self.assertEqual(azure.call_count, 1)

    def test_endpoints_answer_503_over_the_cap(self):
        with self.settings(AI_DAILY_CAPS={"speech": 0}):
            res = self.api.post("/api/ai/read-aloud/", {"text": "Hallo"}, format="json")
        self.assertEqual(res.status_code, 503)
        with (
            self.settings(AI_DAILY_CAPS={"text": 0}),
            mock.patch.object(llm, "_complete", return_value="hi") as complete,
        ):
            res = self.api.post("/api/ai/chat/", {"message": "Hallo"}, format="json")
        self.assertEqual(res.status_code, 503)
        complete.assert_not_called()

    def test_long_messages_and_history_are_limited(self):
        long = "x" * (llm.MAX_MESSAGE_CHARS + 1)
        res = self.api.post("/api/ai/chat/", {"message": long}, format="json")
        self.assertEqual(res.status_code, 400)
        history = [{"role": "user", "content": long}] * 50
        with mock.patch.object(llm, "_complete", return_value="ok") as complete:
            llm.chat("Hallo", history)
        contents = complete.call_args.args[1]
        self.assertEqual(len(contents), llm.MAX_HISTORY_TURNS + 1)
        self.assertEqual(len(contents[0].parts[0].text), llm.MAX_MESSAGE_CHARS)

    def test_oversized_requests_are_refused_unread(self):
        res = self.api.generic(
            "POST", "/api/ai/chat/", b"{}", "application/json", CONTENT_LENGTH=str(50 * 1024 * 1024)
        )
        self.assertEqual(res.status_code, 413)

    def test_placement_submissions_are_limited(self):
        free = APIClient()
        free.force_authenticate(get_user_model().objects.create_user("free", password="pw"))
        codes = [
            free.post("/api/accounts/placement-test/", {}, format="json").status_code
            for _ in range(6)
        ]
        self.assertNotEqual(codes[4], 429)
        self.assertEqual(codes[5], 429)
        self.assertEqual(free.get("/api/accounts/placement-test/").status_code, 200)
