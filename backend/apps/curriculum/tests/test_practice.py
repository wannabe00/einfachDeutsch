"""Practice sets and drills only use what the user has finished."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.books.models import Book, Chapter
from apps.curriculum.content.dsl import fill, group, match, tr
from apps.curriculum.management.commands.seed_a1_path import exercise_fields
from apps.curriculum.models import Lesson, LessonItem, PathLessonProgress, Unit
from apps.exercises.models import Exercise, ExerciseAttempt
from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word


class PracticeTests(TestCase):
    def setUp(self):
        chapter = Chapter.objects.create(book=Book.objects.create(title="T"), number=1, title="L1")
        unit = Unit.objects.create(cefr_level="A1", order=1, title="L1", chapter=chapter)
        self.done = Lesson.objects.create(unit=unit, order=1, title="one")
        self.todo = Lesson.objects.create(unit=unit, order=2, title="two")
        self.rule = GrammarRule.objects.create(chapter=chapter, title="sein")

        def add(lesson, order, item):
            ex = Exercise.objects.create(chapter=chapter, **exercise_fields(item))
            LessonItem.objects.create(lesson=lesson, order=order, exercise=ex)
            return ex

        self.words_ex = add(self.done, 0, tr("the dog", "der Hund", hint="animal"))
        LessonItem.objects.create(lesson=self.done, order=1, kind="grammar", grammar_rule=self.rule)
        sentences = [fill(f"Ich ___ {n}.", "bin") for n in "ABCDEF"]
        self.group_ex = add(self.done, 2, group("Fill in.", *sentences))
        self.match_ex = add(self.done, 3, match([("ja", "yes"), ("nein", "no")]))
        self.future_ex = add(self.todo, 0, tr("the cat", "die Katze"))

        self.hund = Word.objects.create(chapter=chapter, english="dog", german="der Hund")
        self.katze = Word.objects.create(chapter=chapter, english="cat", german="die Katze")
        self.done.words.add(self.hund)
        self.todo.words.add(self.katze)

        self.user = get_user_model().objects.create_user("anna", password="pw")
        PathLessonProgress.objects.create(
            user=self.user, lesson=self.done, completed_at=timezone.now()
        )
        self.api = APIClient()
        self.api.force_authenticate(self.user)

    def start(self, **filters):
        return self.api.post("/api/curriculum/practice/start/", filters, format="json").json()

    def test_set_uses_finished_lessons_without_hints_or_matching(self):
        tasks = self.start()["tasks"]
        ids = {t["task_id"].split(":")[0] for t in tasks}
        self.assertEqual(ids, {str(self.words_ex.id), str(self.group_ex.id)})
        self.assertTrue(all(t["hint"] == "" for t in tasks))
        self.assertNotIn("answer", str(tasks))

    def test_big_groups_are_cut_down(self):
        task = next(t for t in self.start()["tasks"] if t["type"] == "group")
        self.assertLessEqual(len(task["payload"]["parts"]), 4)

    def test_topic_filter_and_options(self):
        opts = self.api.get("/api/curriculum/practice/").json()
        self.assertEqual(opts["topics"], [{"id": self.rule.id, "title": "sein"}])
        tasks = self.start(topic=self.rule.id)["tasks"]
        self.assertEqual({t["task_id"].split(":")[0] for t in tasks}, {str(self.group_ex.id)})

    def test_answer_grades_chosen_parts_and_records_attempt(self):
        res = self.api.post(
            "/api/curriculum/practice/answer/",
            {"task_id": f"{self.group_ex.id}:0,2", "answer": ["bin", "bist"]},
            format="json",
        ).json()
        self.assertEqual(res["parts"], [True, False])
        self.assertEqual(ExerciseAttempt.objects.get(user=self.user).is_correct, False)

    def test_unfinished_lessons_cant_be_answered(self):
        res = self.api.post(
            "/api/curriculum/practice/answer/",
            {"task_id": str(self.future_ex.id), "answer": "die Katze"},
            format="json",
        )
        self.assertEqual(res.status_code, 403)

    def test_drills_get_learned_words_only(self):
        words = self.api.get("/api/vocabulary/words/drill/").json()
        self.assertEqual([w["german"] for w in words], ["der Hund"])
