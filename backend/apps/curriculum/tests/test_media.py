"""Checks on the history and video content files."""

from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from apps.history.content import LESSONS
from apps.videos.content import VIDEOS

HISTORY_IMAGES = Path(settings.BASE_DIR).parent / "frontend" / "public" / "history"
# Words per lesson by level: short and simple at A1, longer as the level rises.
WORDS = {"A1": (120, 220), "A2": (200, 320), "B1": (280, 450)}


class HistoryContentTests(SimpleTestCase):
    def test_lessons(self):
        self.assertEqual(len({lesson["order"] for lesson in LESSONS}), len(LESSONS))
        for lesson in LESSONS:
            title = lesson["title"]
            low, high = WORDS[lesson["level"]]
            self.assertTrue(low <= len(lesson["body_de"].split()) <= high, title)
            self.assertTrue(lesson["body_en"].strip(), title)
            if lesson.get("image"):  # no picture yet: the UI draws the era tile
                self.assertTrue((HISTORY_IMAGES / f"{lesson['image']}.jpg").exists(), title)
            self.assertNotIn("—", str(lesson), title)

    def test_every_level_has_its_own_lessons(self):
        levels = [lesson["level"] for lesson in LESSONS]
        for level in WORDS:
            self.assertGreaterEqual(levels.count(level), 4, level)

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
