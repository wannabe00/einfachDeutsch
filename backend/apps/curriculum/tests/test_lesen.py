"""Lesen: exam-style reading sets, against the real A1 and A2 content."""

import json
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.curriculum import grading
from apps.curriculum.content.levels import LEVELS
from apps.curriculum.exam_sets import set_source
from apps.curriculum.models import PathLessonProgress, ReadingResult, Unit
from apps.exercises.models import Exercise

# Questions per Teil and Teile per set, as in the exams.
SHAPE = {"A1": [5, 5, 5], "A2": [5, 5, 5, 5], "B1": [5, 5, 5, 5]}


class ContentTests(TestCase):
    def test_every_set_has_the_exam_shape_and_valid_answers(self):
        for level, spec in LEVELS.items():
            self.assertEqual(sorted(spec["lesen"]), list(range(1, 9)), level)
            for modul, teile in spec["lesen"].items():
                where = f"{level} Modul {modul}"
                self.assertEqual([len(t["parts"]) for t in teile], SHAPE[level], where)
                for teil in teile:
                    self.assertEqual(teil["type"], "group", where)
                    for part in teil["parts"]:
                        self.assertEqual(part["type"], "multiple_choice", where)
                        self.assertIn(part["answer"], part["options"], f"{where}: {part}")
                        self.assertEqual(len(set(part["options"])), len(part["options"]), where)
                        # Every question has its text: the Teil's or its own.
                        self.assertTrue(teil.get("context") or part.get("context"), where)

    def test_answers_are_not_all_the_same(self):
        """Richtig/falsch and a/b Teile mix their answers."""
        for level, spec in LEVELS.items():
            for modul, teile in spec["lesen"].items():
                for teil in teile:
                    answers = {p["answer"] for p in teil["parts"]}
                    self.assertGreater(len(answers), 1, f"{level} Modul {modul}: {teil['prompt']}")


class LesenFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_path", stdout=StringIO())

    def setUp(self):
        self.user = get_user_model().objects.create_user("anna", password="pw")
        self.user.profile.is_premium = True  # the skills are premium
        self.user.profile.save()
        self.api = APIClient()
        self.api.force_authenticate(self.user)
        self.units = {u.order: u for u in Unit.objects.filter(cefr_level="A1")}

    def finish_units(self, *orders):
        for n in orders:
            for lesson in self.units[n].lessons.all():
                PathLessonProgress.objects.create(
                    user=self.user, lesson=lesson, completed_at=timezone.now()
                )

    def sets(self):
        return self.api.get("/api/curriculum/lesen/").json()

    def right(self, exercise_id):
        exercise = Exercise.objects.get(id=exercise_id)
        return [p["answer"] for p in grading.parts_of(exercise)]

    def test_sets_are_seeded_once(self):
        count = Exercise.objects.filter(source__contains="-lesen-m").count()
        self.assertEqual(count, 8 * 3 + 8 * 4 + 8 * 4)  # A1, A2, B1
        call_command("seed_path", stdout=StringIO())
        self.assertEqual(Exercise.objects.filter(source__contains="-lesen-m").count(), count)

    def test_a1_user_sees_a1_only_and_sets_lock_until_the_modul_is_done(self):
        sets = self.sets()
        self.assertEqual({s["cefr_level"] for s in sets}, {"A1"})
        self.assertEqual(len(sets), 8)
        self.assertTrue(all(s["locked"] for s in sets))
        self.assertEqual(self.api.get("/api/curriculum/lesen/A2/1/").status_code, 404)
        self.assertEqual(self.api.get("/api/curriculum/lesen/A1/1/").status_code, 403)

        self.finish_units(1, 2)
        self.assertTrue(self.sets()[0]["locked"])
        self.finish_units(3)
        sets = self.sets()
        self.assertFalse(sets[0]["locked"])
        self.assertTrue(sets[1]["locked"])

    def test_lower_levels_are_open(self):
        self.user.profile.cefr_level = "A2"
        self.user.profile.save()
        sets = self.sets()
        self.assertEqual([s["cefr_level"] for s in sets], ["A1"] * 8 + ["A2"] * 8)
        self.assertFalse(any(s["locked"] for s in sets if s["cefr_level"] == "A1"))
        self.assertTrue(all(s["locked"] for s in sets if s["cefr_level"] == "A2"))

    def test_answering_grades_and_keeps_the_best(self):
        self.finish_units(1, 2, 3)
        data = self.api.get("/api/curriculum/lesen/a1/1/").json()
        self.assertEqual([t["teil"] for t in data["teile"]], [1, 2, 3])
        self.assertEqual(data["questions"], 15)
        self.assertNotIn('"answer"', json.dumps(data))

        teil = data["teile"][0]
        url = f"/api/curriculum/lesen/teil/{teil['exercise_id']}/answer/"
        right = self.right(teil["exercise_id"])
        res = self.api.post(url, {"answer": right}, format="json").json()
        self.assertEqual(res["parts"], [True] * 5)
        self.assertTrue(res["correct"])
        self.assertEqual(res["solution"], right)

        wrong = ["Falsch" if a == "Richtig" else "Richtig" for a in right]
        res = self.api.post(url, {"answer": wrong}, format="json").json()
        self.assertEqual((res["right"], res["best"]), (0, 5))

        # The set's score shows once every Teil is done.
        self.assertIsNone(self.sets()[0]["best"])
        for t in data["teile"][1:]:
            answer = self.right(t["exercise_id"])
            self.api.post(
                f"/api/curriculum/lesen/teil/{t['exercise_id']}/answer/",
                {"answer": answer},
                format="json",
            )
        first = self.sets()[0]
        self.assertEqual((first["best"], first["questions"], first["passed"]), (15, 15, True))
        self.assertEqual(ReadingResult.objects.filter(user=self.user).count(), 3)

    def test_locked_and_unknown_teile_cannot_be_answered(self):
        locked = Exercise.objects.get(source=set_source("lesen", "A1", 2, 1))
        res = self.api.post(f"/api/curriculum/lesen/teil/{locked.id}/answer/", {"answer": []})
        self.assertEqual(res.status_code, 403)
        other = Exercise.objects.exclude(source__contains="-lesen-m").first()
        res = self.api.post(f"/api/curriculum/lesen/teil/{other.id}/answer/", {"answer": []})
        self.assertEqual(res.status_code, 404)

    def test_guests_are_turned_away(self):
        self.assertEqual(APIClient().get("/api/curriculum/lesen/").status_code, 401)
