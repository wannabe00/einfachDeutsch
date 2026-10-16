"""Hören: exam-style listening sets, their audio manifest and the generator."""

import json
import tempfile
from io import StringIO
from pathlib import Path
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from google.genai import errors
from rest_framework.test import APIClient

from apps.curriculum import hoeren
from apps.curriculum.content.levels import LEVELS
from apps.curriculum.management.commands import make_hoeren_audio
from apps.curriculum.models import PathLessonProgress, Unit
from apps.exercises.models import Exercise

BASE = "/api/curriculum/hoeren"
# (questions, plays) per Teil, as in Start Deutsch 1.
A1_SHAPE = [(6, 2), (4, 1), (5, 2)]


class ContentTests(TestCase):
    def test_a1_sets_have_the_exam_shape(self):
        for modul, teile in LEVELS["A1"]["hoeren"].items():
            where = f"A1 Modul {modul}"
            got = [(len(t["parts"]), t["parts"][0]["clip"]["plays"]) for t in teile]
            # A set may stop early while a Teil waits for its audio (Modul 1 for now).
            self.assertEqual(got, A1_SHAPE[: len(teile)], where)
            self.assertGreaterEqual(len(teile), 2, where)
            for teil in teile:
                answers = {p["answer"] for p in teil["parts"]}
                self.assertGreater(len(answers), 1, f"{where}: {teil['prompt']}")
                for part in teil["parts"]:
                    self.assertIn(part["answer"], part["options"], where)
                    self.assertTrue(part["clip"]["script"], where)

    def test_clip_names_are_unique(self):
        names = [n for n, _, _ in make_hoeren_audio.all_clips(list(LEVELS))]
        self.assertEqual(len(names), len(set(names)))


class HoerenFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_path", stdout=StringIO())

    def setUp(self):
        self.user = get_user_model().objects.create_user("anna", password="pw")
        self.api = APIClient()
        self.api.force_authenticate(self.user)
        units = {u.order: u for u in Unit.objects.filter(cefr_level="A1")}
        for n in (1, 2, 3):
            for lesson in units[n].lessons.all():
                PathLessonProgress.objects.create(
                    user=self.user, lesson=lesson, completed_at=timezone.now()
                )
        self.teile = Exercise.objects.filter(source__contains="-a1-hoeren-m1-").order_by("source")
        names = [n for e in self.teile for n, _ in hoeren.clips_of(e)]
        self.recorded = mock.patch.object(hoeren, "available", return_value=set(names))

    def test_sets_without_audio_are_hidden(self):
        with mock.patch.object(hoeren, "available", return_value=set()):
            self.assertEqual(self.api.get(f"{BASE}/").json(), [])
            self.assertEqual(self.api.get(f"{BASE}/A1/1/").status_code, 404)
        with self.recorded:
            sets = self.api.get(f"{BASE}/").json()
        self.assertEqual([s["modul"] for s in sets], [1])  # Modul 2 isn't recorded here
        # Recorded but not released: hidden too.
        with self.recorded, mock.patch.dict(LEVELS["A1"], {"hoeren_live": set()}):
            self.assertEqual(self.api.get(f"{BASE}/").json(), [])

    def test_audio_without_scripts_or_answers(self):
        with self.recorded:
            data = self.api.get(f"{BASE}/a1/1/").json()
        dumped = json.dumps(data, ensure_ascii=False)
        self.assertNotIn("Schneider", dumped.split('"options"')[0])  # no script before options
        self.assertNotIn('"script"', dumped)
        self.assertNotIn('"answer"', dumped)
        part = data["teile"][0]["payload"]["parts"][0]["payload"]
        self.assertEqual(part["audio"], {"url": "/hoeren/seed-a1-hoeren-m1-t1-0.mp3", "plays": 2})
        self.assertEqual(data["teile"][1]["payload"]["parts"][0]["payload"]["audio"]["plays"], 1)

    def test_answer_reveals_transcripts(self):
        teil = self.teile[0]
        right = [p["answer"] for p in teil.payload["parts"]]
        with self.recorded:
            res = self.api.post(f"{BASE}/teil/{teil.id}/answer/", {"answer": right}, format="json")
        data = res.json()
        self.assertEqual(data["parts"], [True] * 6)
        self.assertEqual(len(data["transcripts"]), 6)
        self.assertEqual(len(self.teile), 2)  # Modul 1 is Teil 1 and 2 for now
        self.assertIn("Frau: Guten Tag!", data["transcripts"][0])


class GeneratorTests(TestCase):
    def setUp(self):
        self.dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.manifest = self.dir / "manifest.json"
        self.enterContext(mock.patch.object(make_hoeren_audio, "AUDIO_DIR", self.dir))
        self.enterContext(mock.patch.object(make_hoeren_audio, "MANIFEST", self.manifest))
        self.enterContext(
            mock.patch.object(make_hoeren_audio, "to_mp3", lambda pcm, path: path.write_bytes(pcm))
        )
        self.enterContext(mock.patch.object(make_hoeren_audio.time, "sleep"))

    def run_cmd(self, *args):
        out = StringIO()
        call_command("make_hoeren_audio", *args, stdout=out)
        return out.getvalue()

    def test_makes_missing_clips_resumes_and_redoes(self):
        with mock.patch.object(
            make_hoeren_audio.llm, "synthesize_speech", return_value=b"pcm"
        ) as tts:
            self.run_cmd("--limit", "2")
            self.run_cmd("--limit", "2")  # the two made are skipped
            self.assertEqual(tts.call_count, 4)
            self.assertEqual(len(json.loads(self.manifest.read_text())), 4)
            self.run_cmd("--redo", "seed-a1-hoeren-m1-t1-0", "--limit", "1")
            self.assertEqual(tts.call_count, 5)

    def test_stops_at_the_quota(self):
        quota = errors.ClientError(
            429, {"error": {"message": "quota", "status": "RESOURCE_EXHAUSTED"}}
        )
        with mock.patch.object(
            make_hoeren_audio.llm, "synthesize_speech", side_effect=[b"pcm", quota, b"pcm"]
        ) as tts:
            out = self.run_cmd()
        self.assertIn("Quota reached", out)
        self.assertEqual(tts.call_count, 2)
        self.assertEqual(len(list(self.dir.glob("*.mp3"))), 1)
