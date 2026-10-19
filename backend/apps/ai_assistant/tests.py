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
