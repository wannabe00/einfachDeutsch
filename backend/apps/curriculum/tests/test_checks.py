"""Checks: Lektion reviews and Modul tests, against the real A1 content."""

import json

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.curriculum import checks, grading
from apps.curriculum.content.dsl import _swap_variant, gap_task, stage_of, translate_task
from apps.curriculum.models import Check, PathLessonProgress, Unit
from apps.vocabulary.models import WordProgress


class SizesAndRampTests(TestCase):
    def test_review_asks_a_third_in_steps_of_five(self):
        self.assertEqual(checks.review_size(30), 10)
        self.assertEqual(checks.review_size(60), 20)
        self.assertEqual(checks.review_size(45), 15)
        self.assertEqual(checks.review_size(12), 5)
        self.assertEqual(checks.review_size(3), 3)
        self.assertEqual(checks.review_size(300), checks.MAX_REVIEW_WORDS)

    def test_ramp(self):
        self.assertEqual([stage_of("A1", n) for n in (1, 6, 7, 12, 13, 24)], [1, 1, 2, 2, 3, 3])
        self.assertEqual(stage_of("A2", 1), 4)

    def test_gaps_are_chips_early_and_typed_later(self):
        early = gap_task(["Ich [heiße] Anna.", "Du [bist] Tom."], ["kommst"], stage=1)
        self.assertEqual(early["type"], "word_bank")
        self.assertEqual(early["answers"], ["heiße", "bist"])
        self.assertIn("kommst", early["bank"])
        late = gap_task([("Ich [heiße] Anna.", "heißen")], stage=3)
        self.assertEqual(late["type"], "fill_blank")
        self.assertEqual(late["hint"], "heißen")

    def test_translations_are_chosen_then_built_then_typed(self):
        pairs = [("I am Anna.", "Ich bin Anna."), ("You are Tom.", "Du bist Tom.")]
        self.assertEqual(translate_task(pairs, 1)["parts"][0]["type"], "multiple_choice")
        self.assertEqual(translate_task(pairs, 2)["parts"][0]["type"], "sentence_order")
        self.assertEqual(translate_task(pairs, 4)["parts"][0]["type"], "translation")
        self.assertEqual(_swap_variant("Ich bin Anna."), "Ich Anna bin.")


class NewTypesGradingTests(TestCase):
    def test_error_spot(self):
        part = {"type": "error_spot", "tokens": ["Ich", "bist"], "answer": "1", "correction": "x"}
        self.assertTrue(grading.grade_part(part, 1))
        self.assertFalse(grading.grade_part(part, 0))
        self.assertNotIn("answer", grading.public_part(part)["payload"])
        self.assertNotIn("correction", grading.public_part(part)["payload"])

    def test_dictation_ignores_punctuation_not_words(self):
        part = {"type": "dictation", "answer": "Komm sofort runter!"}
        self.assertTrue(grading.grade_part(part, "komm sofort runter"))
        self.assertFalse(grading.grade_part(part, "Komm sofort"))
        self.assertFalse(grading.grade_part(part, None))
        self.assertIn("say", grading.public_part(part)["payload"])


class CheckFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_path", stdout=open("/dev/null", "w"))

    def setUp(self):
        self.user = get_user_model().objects.create_user("anna", password="pw")
        self.api = APIClient()
        self.api.force_authenticate(self.user)
        self.units = {u.order: u for u in Unit.objects.filter(cefr_level="A1")}

    def finish_units(self, *orders):
        for n in orders:
            for lesson in self.units[n].lessons.all():
                PathLessonProgress.objects.create(
                    user=self.user, lesson=lesson, completed_at=timezone.now()
                )

    def start(self, **data):
        return self.api.post("/api/curriculum/checks/start/", data, format="json")

    def right_answer(self, task_id):
        """The correct answer for a task, read from the server side."""
        parts, exercise, _ = checks._Loaded([task_id]).task(task_id)

        def one(part):
            ptype = part["type"]
            if ptype == "matching":
                return dict(part["pairs"])
            if ptype == "word_bank":
                return part["answers"]
            if ptype in ("multiple_choice", "sentence_order", "error_spot"):
                return part["answer"]
            return grading._accepted(part)[0]

        if exercise is not None and exercise.exercise_type != "group":
            return one(parts[0])
        return one(parts[0]) if len(parts) == 1 and exercise is None else [one(p) for p in parts]

    def test_review_needs_a_finished_lektion(self):
        res = self.start(kind="review", unit=self.units[1].id)
        self.assertEqual(res.status_code, 403)

    def test_review_of_a_finished_lektion(self):
        self.finish_units(1)
        status = self.api.get("/api/curriculum/checks/").json()
        self.assertEqual(status["last_unit"]["order"], 1)

        data = self.start(kind="review", unit=self.units[1].id).json()
        word_tasks = [t for t in data["tasks"] if not t["task_id"].startswith("e:")]
        authored = [t for t in data["tasks"] if t["task_id"].startswith("e:")]
        learned = self.units[1].chapter.words.count()
        asked = sum(
            len(t["payload"]["parts"]) if t["type"] == "group" else len(t["payload"]["left"])
            for t in word_tasks
        )
        self.assertEqual(asked, checks.review_size(learned))
        self.assertTrue(all(len(t["task_id"].split(",")) <= checks.BATCH for t in word_tasks))
        self.assertEqual(len(authored), 2)  # the gap task and the translation task
        # No answers reach the client.
        self.assertNotIn('"answer"', json.dumps(data["tasks"]))
        self.assertNotIn('"answers"', json.dumps(data["tasks"]))

        # Resuming gives the same check.
        self.assertEqual(self.start(kind="review", unit=self.units[1].id).json()["id"], data["id"])

        url = f"/api/curriculum/checks/{data['id']}"
        self.assertEqual(self.api.post(f"{url}/finish/").status_code, 403)
        for task in data["tasks"]:
            res = self.api.post(
                f"{url}/answer/",
                {"task_id": task["task_id"], "answer": self.right_answer(task["task_id"])},
                format="json",
            ).json()
            self.assertTrue(res["correct"], task)

        self.assertEqual(WordProgress.objects.filter(user=self.user).count(), asked)
        done = self.api.post(f"{url}/finish/").json()
        self.assertEqual(done["score"], 1)
        self.assertTrue(done["completed"])
        self.assertIn("words", done["skills"])

    def test_a_task_from_another_check_is_refused(self):
        self.finish_units(1)
        data = self.start(kind="review", unit=self.units[1].id).json()
        res = self.api.post(
            f"/api/curriculum/checks/{data['id']}/answer/",
            {"task_id": "e:1", "answer": "x"},
            format="json",
        )
        self.assertEqual(res.status_code, 403)

    def test_wrong_word_answers_count_as_lapses(self):
        self.finish_units(1)
        data = self.start(kind="review", unit=self.units[1].id).json()
        task = next(t for t in data["tasks"] if t["task_id"].startswith(("w:", "m:")))
        wrong = [] if task["type"] == "group" else {}
        self.api.post(
            f"/api/curriculum/checks/{data['id']}/answer/",
            {"task_id": task["task_id"], "answer": wrong},
            format="json",
        )
        lapses = WordProgress.objects.filter(user=self.user).values_list("lapses", flat=True)
        self.assertTrue(lapses and all(n == 1 for n in lapses))

    def test_modul_test_unlocks_after_three_lektionen(self):
        self.finish_units(1, 2)
        modul = self.api.get("/api/curriculum/checks/").json()["moduls"][0]
        self.assertFalse(modul["unlocked"])
        self.assertEqual(self.start(kind="modul", level="A1", modul=1).status_code, 403)

        self.finish_units(3)
        modul = self.api.get("/api/curriculum/checks/").json()["moduls"][0]
        self.assertTrue(modul["unlocked"])
        data = self.start(kind="modul", level="A1", modul=1).json()
        skills = {t["skill"] for t in data["tasks"]}
        self.assertEqual(skills, {"words", "grammar", "reading"})  # no listening at stage 1
        self.assertEqual(Check.objects.get(id=data["id"]).kind, "modul")

    def test_later_modul_tests_mix_in_earlier_content_and_listening(self):
        self.finish_units(*range(1, 16))
        data = self.start(kind="modul", level="A1", modul=5).json()
        types = {t["type"] for t in data["tasks"]}
        self.assertIn("group", types)
        self.assertIn("listening", {t["skill"] for t in data["tasks"]})
        parts = [p for t in data["tasks"] for p in t["payload"].get("parts", [])]
        self.assertIn("error_spot", {p["type"] for p in parts})

    def test_every_authored_task_is_solvable(self):
        from apps.exercises.models import Exercise

        authored = Exercise.objects.filter(source__contains="-check-")
        for level in ("a1", "a2"):
            # A gap task and a translation task for each of the 24 Lektionen.
            lektion_tasks = authored.filter(source__startswith=f"seed-{level}-check-u")
            self.assertEqual(lektion_tasks.count(), 48, level)
        for exercise in authored:
            answer = self.right_answer(f"e:{exercise.id}")
            self.assertTrue(all(grading.grade_parts(exercise, answer)), exercise.source)

    def test_a2_review_uses_typed_formats(self):
        self.user.profile.cefr_level = "A2"
        self.user.profile.save()
        unit = Unit.objects.get(cefr_level="A2", order=1)
        for lesson in unit.lessons.all():
            PathLessonProgress.objects.create(
                user=self.user, lesson=lesson, completed_at=timezone.now()
            )
        data = self.start(kind="review", unit=unit.id).json()
        types = {t["type"] for t in data["tasks"]}
        self.assertNotIn("matching", types)  # stage 4: no matching batches
        authored = [t for t in data["tasks"] if t["task_id"].startswith("e:")]
        parts = [p["type"] for t in authored for p in t["payload"].get("parts", [t])]
        self.assertEqual(set(parts), {"fill_blank", "translation"})
        # A1 counts as learned below the user's level, so every A1 Modul test is open.
        moduls = self.api.get("/api/curriculum/checks/").json()["moduls"]
        self.assertTrue(all(m["unlocked"] for m in moduls if m["cefr_level"] == "A1"))
