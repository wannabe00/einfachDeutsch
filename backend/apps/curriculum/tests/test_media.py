"""Checks on the history and video content files."""

from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from apps.history.content import LESSONS
from apps.videos.content import VIDEOS

HISTORY_IMAGES = Path(settings.BASE_DIR).parent / "frontend" / "public" / "history"


class HistoryContentTests(SimpleTestCase):
    def test_lessons(self):
        self.assertEqual(len({lesson["order"] for lesson in LESSONS}), len(LESSONS))
        for lesson in LESSONS:
            title = lesson["title"]
            self.assertGreaterEqual(len(lesson["body_de"].split()), 230, title)
            self.assertTrue(lesson["body_en"].strip(), title)
            self.assertTrue((HISTORY_IMAGES / f"{lesson['image']}.jpg").exists(), title)
            self.assertNotIn("—", str(lesson), title)

    def test_quiz_has_five_answerable_questions(self):
        for lesson in LESSONS:
            self.assertEqual(len(lesson["quiz"]), 5, lesson["title"])
            for q in lesson["quiz"]:
                self.assertIn(q["answer"], q["options"], q["prompt"])
                self.assertEqual(len(set(q["options"])), len(q["options"]), q["prompt"])


class VideoContentTests(SimpleTestCase):
    def test_every_pick_is_described(self):
        for video in VIDEOS:
            for field in ("description", "audience", "format", "cost", "tips", "url"):
                self.assertTrue(video.get(field), f"{video['title']}: {field}")
            if video["platform"] == "YouTube":
                self.assertTrue(
                    video["image_url"].startswith("https://i.ytimg.com/"), video["title"]
                )
            self.assertNotIn("—", str(video), video["title"])
