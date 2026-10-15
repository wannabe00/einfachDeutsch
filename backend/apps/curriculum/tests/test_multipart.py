"""Multi-part exercises through the lesson player and the level exam."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.books.models import Book, Chapter
from apps.curriculum.content.dsl import art, fill, group
from apps.curriculum.management.commands.seed_path import exercise_fields
from apps.curriculum.models import Lesson, LessonItem, PathLessonProgress, Unit
from apps.exercises.models import Exercise


class LessonFixture(TestCase):
    """One lesson: a four-part article group, then a single fill-in."""

    def setUp(self):
        chapter = Chapter.objects.create(book=Book.objects.create(title="T"), number=1, title="L1")
        unit = Unit.objects.create(cefr_level="A1", order=1, title="L1", chapter=chapter)
        self.lesson = Lesson.objects.create(unit=unit, order=1, title="one")
        parts = [art("der Tisch"), art("die Lampe"), art("das Buch"), art("der Stuhl")]
        self.group = Exercise.objects.create(
            chapter=chapter, **exercise_fields(group("Choose the article.", *parts))
        )
        self.single = Exercise.objects.create(
            chapter=chapter, **exercise_fields(fill("Ich ___ Anna.", "bin"))
        )
        self.group_item = LessonItem.objects.create(
            lesson=self.lesson, order=0, exercise=self.group
        )
        self.single_item = LessonItem.objects.create(
            lesson=self.lesson, order=1, exercise=self.single
        )

        user = get_user_model().objects.create_user("anna", password="pw")
        user.profile.is_premium = True
        user.profile.save()
        self.user = user
        self.api = APIClient()
        self.api.force_authenticate(user)

    def url(self, action=""):
        return f"/api/curriculum/lessons/{self.lesson.id}/{action}"


class MultiPartTests(LessonFixture):
    def test_lesson_sends_parts_without_answers(self):
        items = self.api.get(self.url()).json()["items"]
        content = items[0]["content"]
        self.assertEqual(content["type"], "group")
        self.assertEqual([p["prompt"] for p in content["payload"]["parts"]][0], "___ Tisch")
        self.assertNotIn("answer", str(content))

    def test_answer_marks_each_part(self):
        res = self.api.post(
            self.url("answer/"),
            {"item_id": self.group_item.id, "answer": ["der", "der", "das", "der"]},
            format="json",
        ).json()
        self.assertFalse(res["correct"])
        self.assertEqual(res["parts"], [True, False, True, True])
        self.assertEqual(res["solution"], [["der"], ["die"], ["das"], ["der"]])

    def test_score_counts_parts(self):
        answers = [
            {"item_id": self.group_item.id, "answer": ["der", "der", "das", "der"]},
            {"item_id": self.single_item.id, "answer": "bin"},
        ]
        res = self.api.post(self.url("complete/"), {"answers": answers}, format="json").json()
        self.assertEqual((res["correct"], res["total"]), (4, 5))
        self.assertTrue(res["passed"])

    def test_exam_asks_single_parts_and_grades_them(self):
        PathLessonProgress.objects.create(
            user=self.user, lesson=self.lesson, completed_at="2026-01-01T00:00Z"
        )
        status = self.api.get("/api/curriculum/exam/").json()
        self.assertEqual(status["question_count"], 5)  # 4 parts + 1 single exercise

        start = self.api.post("/api/curriculum/exam/start/").json()
        refs = {q["question_id"]: q for q in start["questions"]}
        self.assertEqual(
            set(refs), {f"{self.group.id}:{i}" for i in range(4)} | {str(self.single.id)}
        )
        self.assertNotIn("group", {q["type"] for q in refs.values()})

        solutions = {
            f"{self.group.id}:0": "der",
            f"{self.group.id}:1": "die",
            f"{self.group.id}:2": "das",
            f"{self.group.id}:3": "die",  # wrong
            str(self.single.id): "bin",
        }
        res = self.api.post(
            "/api/curriculum/exam/submit/",
            {"attempt_id": start["attempt_id"], "answers": solutions},
            format="json",
        ).json()
        self.assertEqual((res["correct"], res["total"]), (4, 5))


class SavedProgressTests(LessonFixture):
    """A lesson can be left and resumed; finishing it clears what was saved."""

    def check(self, item, answer):
        self.api.post(self.url("answer/"), {"item_id": item.id, "answer": answer}, format="json")

    def test_checked_answers_are_saved_and_returned(self):
        self.assertIsNone(self.api.get(self.url()).json()["saved"])
        self.check(self.group_item, ["der", "die", "das", "der"])

        saved = self.api.get(self.url()).json()["saved"]
        self.assertEqual(saved["step"], 1)
        self.assertEqual(saved["answers"], {str(self.group_item.id): ["der", "die", "das", "der"]})

    def test_complete_uses_saved_answers_and_clears_them(self):
        self.check(self.group_item, ["der", "die", "das", "der"])
        # After resuming, the client only sends what it answered since.
        answers = [{"item_id": self.single_item.id, "answer": "bin"}]
        res = self.api.post(self.url("complete/"), {"answers": answers}, format="json").json()
        self.assertEqual((res["correct"], res["total"]), (5, 5))
        self.assertIsNone(self.api.get(self.url()).json()["saved"])

    def test_restart_forgets_saved_answers(self):
        self.check(self.group_item, ["der", "die", "das", "der"])
        self.api.delete(self.url("restart/"))
        self.assertIsNone(self.api.get(self.url()).json()["saved"])
