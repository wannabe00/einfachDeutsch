"""Schreiben: exam-style writing sets, the rubric, and the self/AI grading flow."""

import json
from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.ai_assistant.llm import AIConfigError, AIResponseError
from apps.curriculum import schreiben
from apps.curriculum.content.levels import LEVELS
from apps.curriculum.exam_sets import set_source
from apps.curriculum.models import PathLessonProgress, Unit, WritingAttempt
from apps.exercises.models import Exercise

BASE = "/api/curriculum/schreiben"


class ContentTests(TestCase):
    def test_every_set_has_the_exam_shape(self):
        for level, spec in LEVELS.items():
            self.assertEqual(sorted(spec["schreiben"]), list(range(1, 9)), level)
            for modul, (teil1, teil2) in spec["schreiben"].items():
                where = f"{level} Modul {modul}"
                if level == "A1":
                    self.assertEqual(teil1["type"], "group", where)
                    self.assertEqual(len(teil1["parts"]), 5, where)
                    self.assertTrue(all(p["type"] == "fill_blank" for p in teil1["parts"]))
                    self.assertTrue(teil1["context"], where)
                    texts = [teil2]
                else:
                    self.assertEqual((teil1["min_words"], teil1["max_words"]), (20, 30), where)
                    self.assertEqual((teil2["min_words"], teil2["max_words"]), (30, 40), where)
                    self.assertTrue(teil2["formal"], where)
                    texts = [teil1, teil2]
                for task in texts:
                    self.assertEqual(task["type"], "free_text", where)
                    self.assertEqual(len(task["points"]), 3, where)

    def test_model_answers_fit_their_task(self):
        """Every model answer is in its word range, with a greeting and a sign-off."""
        for level, spec in LEVELS.items():
            for modul, teile in spec["schreiben"].items():
                for task in teile:
                    if task["type"] != "free_text":
                        continue
                    check = schreiben.checks(task["model"], task)
                    where = f"{level} Modul {modul}: {task['model'][:40]}"
                    self.assertTrue(check["in_range"], f"{where} ({check['words']} words)")
                    self.assertTrue(check["greeting"], where)
                    self.assertTrue(check["closing"], where)


class RubricTests(TestCase):
    TASK = {"min_words": 20, "max_words": 30}

    def check(self, text):
        return schreiben.checks(text, self.TASK)

    def test_words_greeting_and_closing(self):
        c = self.check("Hallo Ben,\nich komme um 8 Uhr. Wie geht's?\nBis gleich, Tom")
        self.assertEqual(c["words"], 12)
        self.assertTrue(c["greeting"] and c["closing"])
        self.assertFalse(c["too_short"])  # 12 is not under half of 20
        c = self.check("ich komme morgen nicht")
        self.assertFalse(c["greeting"] or c["closing"])
        self.assertTrue(c["too_short"])

    def test_a1_points_and_communication(self):
        full = {"too_short": False, "greeting": True, "closing": True}
        self.assertEqual(schreiben.a1_score(["full"] * 3, full)[:2], (10, 10))
        half = {**full, "closing": False}
        self.assertEqual(schreiben.a1_score(["full", "partial", "missing"], half)[0], 5)

    def test_a2_task_letters_follow_the_official_table(self):
        letter = schreiben.a2_task_letter
        self.assertEqual(letter(["full", "full", "full"]), "A")
        self.assertEqual(letter(["full", "full", "missing"]), "B")
        self.assertEqual(letter(["full", "partial", "partial"]), "B")
        self.assertEqual(letter(["full", "partial", "missing"]), "C")
        self.assertEqual(letter(["partial", "partial", "partial"]), "C")
        self.assertEqual(letter(["full", "missing", "missing"]), "D")
        self.assertEqual(letter(["missing"] * 3), "E")

    def test_a2_scores(self):
        ok = {"too_short": False}
        self.assertEqual(schreiben.a2_score(["full"] * 3, ok, "B")[:2], (8.5, 10))
        self.assertEqual(schreiben.a2_score(["full"] * 3, ok, None)[:2], (5, 5))  # self-check
        # Task E (or too short) is 0 for the whole Teil, language included.
        self.assertEqual(schreiben.a2_score(["missing"] * 3, ok, "A")[0], 0)
        self.assertEqual(schreiben.a2_score(["full"] * 3, {"too_short": True}, "A")[0], 0)


class SchreibenFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_path", stdout=StringIO())

    def setUp(self):
        self.user = get_user_model().objects.create_user("anna", password="pw")
        self.api = APIClient()
        self.api.force_authenticate(self.user)
        self.units = {u.order: u for u in Unit.objects.filter(cefr_level="A1")}
        for n in (1, 2, 3):
            for lesson in self.units[n].lessons.all():
                PathLessonProgress.objects.create(
                    user=self.user, lesson=lesson, completed_at=timezone.now()
                )
        self.form = Exercise.objects.get(source=set_source("schreiben", "A1", 1, 1))
        self.message = Exercise.objects.get(source=set_source("schreiben", "A1", 1, 2))

    def write(self, text, exercise=None):
        exercise = exercise or self.message
        return self.api.post(f"{BASE}/teil/{exercise.id}/write/", {"text": text}, format="json")

    def premium(self):
        self.user.profile.is_premium = True
        self.user.profile.save()

    def test_sets_are_seeded_and_locked_like_lesen(self):
        self.assertEqual(Exercise.objects.filter(source__contains="-schreiben-m").count(), 32)
        sets = self.api.get(f"{BASE}/").json()
        self.assertEqual([s["locked"] for s in sets], [False] + [True] * 7)
        self.assertEqual(self.api.get(f"{BASE}/A1/2/").status_code, 403)
        self.assertEqual(self.api.get(f"{BASE}/A2/1/").status_code, 404)

    def test_no_answers_or_model_text_before_writing(self):
        data = self.api.get(f"{BASE}/a1/1/").json()
        self.assertEqual([t["type"] for t in data["teile"]], ["group", "free_text"])
        dumped = json.dumps(data, ensure_ascii=False)
        self.assertNotIn('"answer"', dumped)
        self.assertNotIn('"model"', dumped)
        self.assertNotIn("Marco Rossi", dumped)

    def test_form_is_graded_locally(self):
        answers = ["costa", "27 Jahre", "Brasilien", "Ärztin", "ledig"]
        res = self.api.post(f"{BASE}/teil/{self.form.id}/form/", {"answer": answers}, format="json")
        data = res.json()
        self.assertEqual(data["parts"], [True, True, True, True, False])
        self.assertEqual((data["attempt"]["score"], data["attempt"]["max_score"]), (4, 5))

    def test_write_then_self_check(self):
        text = (
            "Guten Tag, Frau Berg,\nich heiße Ana und komme aus Brasilien. Ich wohne in "
            "Köln und spreche Portugiesisch und Englisch.\nViele Grüße\nAna"
        )
        data = self.write(text).json()
        self.assertIn("Marco Rossi", data["model"])  # shown only now
        attempt = data["attempt"]
        self.assertIsNone(attempt["score"])
        self.assertTrue(attempt["feedback"]["checks"]["greeting"])

        url = f"{BASE}/attempts/{attempt['id']}/self/"
        self.assertEqual(self.api.post(url, {"points": ["full"]}, format="json").status_code, 400)
        res = self.api.post(url, {"points": ["full", "full", "partial"]}, format="json").json()
        self.assertEqual((res["score"], res["max_score"], res["graded_by"]), (8.5, 10, "self"))
        # Graded once; the set now shows its best.
        self.assertEqual(
            self.api.post(url, {"points": ["full"] * 3}, format="json").status_code, 400
        )
        teil = self.api.get(f"{BASE}/").json()[0]["teile"][1]
        self.assertEqual(teil["best"]["score"], 8.5)

    def test_far_too_short_is_zero_at_once(self):
        attempt = self.write("Hallo, ich bin Ana.").json()["attempt"]
        self.assertEqual((attempt["score"], attempt["graded_by"]), (0, "auto"))

    def test_attempts_are_kept_and_private(self):
        self.write("Hallo Frau Berg, ich bin Ana aus Brasilien und wohne in Köln. Tschüs")
        self.write("Hallo Frau Berg, ich heiße Ana. Ich spreche Englisch. Viele Grüße, Ana")
        rows = self.api.get(f"{BASE}/teil/{self.message.id}/attempts/").json()
        self.assertEqual(len(rows), 2)
        other = get_user_model().objects.create_user("ben", password="pw")
        attempt = WritingAttempt.objects.filter(user=self.user).first()
        api = APIClient()
        api.force_authenticate(other)
        res = api.post(
            f"{BASE}/attempts/{attempt.id}/self/", {"points": ["full"] * 3}, format="json"
        )
        self.assertEqual(res.status_code, 400)

    def test_ai_grading_is_premium_and_scored_by_the_rubric(self):
        attempt = self.write(
            "Guten Tag, Frau Berg,\nich bin Ana aus Brasilien und wohne in Köln.\nGruß, Ana"
        )
        url = f"{BASE}/attempts/{attempt.json()['attempt']['id']}/ai/"
        self.assertEqual(self.api.post(url).status_code, 403)

        self.premium()
        graded = {
            "points": ["full", "full", "missing"],
            "comments": ["ok", "ok", "Say which languages you speak."],
            "language": "A",
            "corrected": "Guten Tag, Frau Berg, …",
            "tips": ["Name your languages."],
        }
        with mock.patch("apps.curriculum.schreiben.llm.grade_writing", return_value=graded):
            res = self.api.post(url).json()
        self.assertEqual((res["score"], res["graded_by"]), (7, "ai"))  # 3 + 3 + 0 + 1
        self.assertEqual(res["feedback"]["tips"], ["Name your languages."])

    def test_ai_errors_save_nothing(self):
        self.premium()
        attempt = self.write(
            "Guten Tag, Frau Berg,\nich bin Ana aus Brasilien und wohne in Köln.\nGruß, Ana"
        )
        url = f"{BASE}/attempts/{attempt.json()['attempt']['id']}/ai/"
        with mock.patch(
            "apps.curriculum.schreiben.llm.grade_writing", side_effect=AIConfigError("no key")
        ):
            self.assertEqual(self.api.post(url).status_code, 503)
        with mock.patch(
            "apps.curriculum.schreiben.llm.grade_writing", side_effect=AIResponseError("bad")
        ):
            self.assertEqual(self.api.post(url).status_code, 502)
        self.assertEqual(WritingAttempt.objects.get(user=self.user).graded_by, "")
