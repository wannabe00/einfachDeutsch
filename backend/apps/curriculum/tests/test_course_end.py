"""B1 is the last level: its exam finishes the course instead of promoting."""

from django.test import SimpleTestCase

from apps.accounts.levels import COURSE_LEVELS, cap_level
from apps.curriculum.exam import next_level_of
from apps.curriculum.models import PathLessonProgress, Unit

from .test_multipart import LessonFixture


class LadderTests(SimpleTestCase):
    def test_the_ladder_stops_at_b1(self):
        self.assertEqual(COURSE_LEVELS, ["A1", "A2", "B1"])
        self.assertEqual((next_level_of("A1"), next_level_of("A2")), ("A2", "B1"))
        self.assertIsNone(next_level_of("B1"))
        self.assertEqual((cap_level("C1"), cap_level("A2")), ("B1", "A2"))


class CourseEndTests(LessonFixture):
    def setUp(self):
        super().setUp()
        Unit.objects.update(cefr_level="B1")
        self.user.profile.cefr_level = "B1"
        self.user.profile.save()
        PathLessonProgress.objects.create(
            user=self.user, lesson=self.lesson, completed_at="2026-01-01T00:00Z"
        )

    def test_passing_b1_completes_the_course_without_promoting(self):
        self.assertFalse(self.api.get("/api/curriculum/exam/").json()["course_complete"])
        start = self.api.post("/api/curriculum/exam/start/").json()
        right = {f"{self.group.id}:{i}": a for i, a in enumerate(["der", "die", "das", "der"])}
        right[str(self.single.id)] = "bin"
        res = self.api.post(
            "/api/curriculum/exam/submit/",
            {"attempt_id": start["attempt_id"], "answers": right},
            format="json",
        ).json()
        self.assertTrue(res["passed"] and res["course_complete"])
        self.assertIsNone(res["promoted_to"])
        self.assertEqual(res["level"], "B1")
        status = self.api.get("/api/curriculum/exam/").json()
        self.assertTrue(status["course_complete"])
        self.assertIsNone(status["next_level"])

    def test_levels_above_b1_cant_be_chosen(self):
        self.user.profile.level_set = False
        self.user.profile.save()
        res = self.api.post("/api/accounts/set-level/", {"cefr_level": "B2"}, format="json")
        self.assertEqual(res.status_code, 400)
