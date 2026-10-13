"""AI-written history lessons: the rules enforced in code (history.custom)."""

from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.history import custom, images
from apps.history.models import CustomHistoryLesson

URL = "/api/history/custom/"


def lesson(words=160, on_topic=True, quiz=None):
    return {
        "on_topic": on_topic,
        "title": "Die Brüder Grimm",
        "era": "19. Jahrhundert",
        "excerpt": "Zwei Brüder sammeln Märchen.",
        "body_de": " ".join(["Wort"] * words),
        "body_en": "Two brothers collect fairy tales.",
        "quiz": quiz
        if quiz is not None
        else [
            {
                "prompt": f"Frage {i}?",
                "options": ["ja", "nein", "vielleicht", "nie"],
                "answer": "ja",
            }
            for i in range(5)
        ],
        "image_query": "Brothers Grimm",
    }


@override_settings(REST_FRAMEWORK={"DEFAULT_THROTTLE_CLASSES": [], "DEFAULT_THROTTLE_RATES": {}})
class CustomHistoryTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("anna", password="pw")
        self.user.profile.is_premium = True
        self.user.profile.save()
        self.api = APIClient()
        self.api.force_authenticate(self.user)
        patcher = mock.patch.object(
            custom, "find_image", return_value=("https://upload.wikimedia.org/x.jpg", "A, CC0")
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        # The AI views are throttled; tests call them freely.
        throttles = mock.patch(
            "apps.history.views.CustomLessonViewSet.get_throttles", return_value=[]
        )
        throttles.start()
        self.addCleanup(throttles.stop)

    def chat(self, *messages):
        return self.api.post(f"{URL}chat/", {"messages": list(messages)}, format="json")

    def test_free_users_are_locked_out(self):
        self.user.profile.is_premium = False
        self.user.profile.save()
        self.assertEqual(self.api.get(URL).status_code, 403)

    @mock.patch("apps.ai_assistant.llm.history_lesson_guide")
    def test_chat_passes_the_guide_result_through(self, guide):
        guide.return_value = {"status": "ready", "reply": "Gern!", "topic": "Die Brüder Grimm"}
        res = self.chat({"role": "user", "content": "the Grimm brothers"}).json()
        self.assertEqual(res, {"status": "ready", "reply": "Gern!", "topic": "Die Brüder Grimm"})

    @mock.patch("apps.ai_assistant.llm.history_lesson_guide")
    def test_chat_refusal_has_no_topic(self, guide):
        guide.return_value = {"status": "refuse", "reply": "Only Germany.", "topic": "Pizza"}
        res = self.chat({"role": "user", "content": "Italian pizza"}).json()
        self.assertEqual((res["status"], res["topic"]), ("refuse", ""))

    def test_chat_rejects_long_or_malformed_input(self):
        self.assertEqual(self.chat({"role": "user", "content": "x" * 501}).status_code, 400)
        self.assertEqual(self.chat({"role": "system", "content": "hi"}).status_code, 400)

    @mock.patch("apps.ai_assistant.llm.write_history_lesson", return_value=lesson())
    def test_create_saves_a_checked_lesson(self, _):
        res = self.api.post(URL, {"topic": "Die Brüder Grimm"}, format="json")
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["image_url"], "https://upload.wikimedia.org/x.jpg")
        self.assertNotIn("answer", str(data["quiz"]))
        self.assertEqual(data["cefr_level"], "A1")

        graded = self.api.post(
            f"{URL}{data['id']}/complete/",
            {"answers": {str(i): "ja" for i in range(5)}},
            format="json",
        ).json()
        self.assertEqual(graded["score"], 100)

    @mock.patch("apps.ai_assistant.llm.write_history_lesson", return_value=lesson(on_topic=False))
    def test_off_topic_lessons_are_refused(self, _):
        res = self.api.post(URL, {"topic": "Pizza"}, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertFalse(CustomHistoryLesson.objects.exists())

    def test_broken_lessons_are_never_saved(self):
        bad = [
            lesson(words=900),  # far too long for A1
            lesson(quiz=[{"prompt": "?", "options": ["a", "a", "b", "c"], "answer": "a"}] * 5),
            lesson(quiz=[{"prompt": "?", "options": ["a", "b", "c", "d"], "answer": "z"}] * 5),
            lesson(quiz=[]),
        ]
        for data in bad:
            with mock.patch("apps.ai_assistant.llm.write_history_lesson", return_value=data) as w:
                res = self.api.post(URL, {"topic": "Grimm"}, format="json")
                self.assertEqual(res.status_code, 502)
                self.assertEqual(w.call_count, custom.ATTEMPTS)
        self.assertFalse(CustomHistoryLesson.objects.exists())

    @mock.patch("apps.ai_assistant.llm.write_history_lesson", return_value=lesson())
    def test_daily_limit(self, _):
        for _ in range(custom.DAILY_LIMIT):
            self.assertEqual(self.api.post(URL, {"topic": "Grimm"}, format="json").status_code, 201)
        self.assertEqual(self.api.post(URL, {"topic": "Grimm"}, format="json").status_code, 429)

    @mock.patch("apps.ai_assistant.llm.write_history_lesson", return_value=lesson())
    def test_lessons_are_private(self, _):
        lesson_id = self.api.post(URL, {"topic": "Grimm"}, format="json").json()["id"]
        other = get_user_model().objects.create_user("ben", password="pw")
        other.profile.is_premium = True
        other.profile.save()
        api = APIClient()
        api.force_authenticate(other)
        self.assertEqual(api.get(f"{URL}{lesson_id}/").status_code, 404)
        self.assertEqual(api.get(URL).json(), [])


class ImageSearchTests(TestCase):
    def page(self, index, license_name, mime="image/jpeg"):
        return {
            "index": index,
            "imageinfo": [
                {
                    "mime": mime,
                    "width": 1200,
                    "thumburl": f"https://upload.wikimedia.org/{index}.jpg",
                    "extmetadata": {
                        "LicenseShortName": {"value": license_name},
                        "Artist": {"value": "<a href='x'>Jane</a>"},
                    },
                }
            ],
        }

    def test_only_free_licences_are_used(self):
        pages = {
            "1": self.page(1, "Fair use"),
            "2": self.page(2, "CC BY-NC 4.0"),
            "3": self.page(3, "CC BY-SA 4.0"),
        }
        with mock.patch.object(images, "_get", return_value={"query": {"pages": pages}}):
            url, credit = images.find_image("castle")
        self.assertEqual(url, "https://upload.wikimedia.org/3.jpg")
        self.assertEqual(credit, "Jane, CC BY-SA 4.0, Wikimedia Commons")

    def test_network_errors_mean_no_picture(self):
        with mock.patch.object(images, "_get", side_effect=OSError):
            self.assertEqual(images.find_image("castle"), ("", ""))
