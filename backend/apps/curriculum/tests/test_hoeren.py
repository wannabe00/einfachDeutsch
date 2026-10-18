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
from rest_framework.test import APIClient

from apps.curriculum import hoeren
from apps.curriculum.content.levels import LEVELS
from apps.curriculum.management.commands import make_hoeren_audio
from apps.curriculum.models import PathLessonProgress, Unit
from apps.exercises.models import Exercise

BASE = "/api/curriculum/hoeren"
# (questions, plays) per Teil: a long conversation, five announcements, a long phone message.
A1_SHAPE = [(5, 2), (5, 1), (5, 2)]
# The first Modul 1 (short clips), live until the new one is recorded.
A1_LIVE_M1 = [(6, 2), (4, 1)]


# A2 like Goethe A2: Teil 2 and 4 are one recording for the whole Teil.
A2_SHAPE = [(5, 2), (5, 1), (5, 1), (5, 2)]


def _plays(teil):
    return (teil.get("clip") or teil["parts"][0]["clip"])["plays"]


class ContentTests(TestCase):
    def test_a2_sets_have_the_exam_shape(self):
        for modul, teile in LEVELS["A2"]["hoeren"].items():
            where = f"A2 Modul {modul}"
            self.assertEqual([(len(t["parts"]), _plays(t)) for t in teile], A2_SHAPE, where)
            for teil in teile:
                self.assertGreater(len({p["answer"] for p in teil["parts"]}), 1, where)
                for part in teil["parts"]:
                    self.assertIn(part["answer"], part["options"], where)
            self.assertTrue(teile[1]["context"] and teile[1]["clip"], where)  # choices + one talk

    def test_a1_sets_have_the_exam_shape(self):
        spec = LEVELS["A1"]
        sets = [(f"A1 Modul {m}", t) for m, t in spec["hoeren"].items() if m != 1]
        sets += [(f"A1 Modul {m} (next)", t) for m, t in spec["hoeren_next"].items()]
        for where, teile in sets:
            self.assertEqual([(len(t["parts"]), _plays(t)) for t in teile], A1_SHAPE, where)
            self.assertTrue(teile[0]["clip"] and teile[2]["clip"]["phone"], where)  # long ones
            for teil in teile:
                answers = {p["answer"] for p in teil["parts"]}
                self.assertGreater(len(answers), 1, f"{where}: {teil['prompt']}")
                for part in teil["parts"]:
                    self.assertIn(part["answer"], part["options"], where)
        live = spec["hoeren"][1]
        self.assertEqual([(len(t["parts"]), _plays(t)) for t in live], A1_LIVE_M1)

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
        first = hoeren.clips_of(self.teile[0])[0][0]
        self.assertEqual(part["audio"], {"url": f"/hoeren/{first}.mp3", "plays": 2})
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
        self.enterContext(mock.patch.object(make_hoeren_audio, "SCENE_DIR", self.dir))
        self.enterContext(
            mock.patch.object(
                make_hoeren_audio, "to_mp3", lambda pcm, path, rec: path.write_bytes(pcm)
            )
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
            first = make_hoeren_audio.all_clips(list(LEVELS))[0][0]
            self.run_cmd("--redo", first, "--limit", "1")
            self.assertEqual(tts.call_count, 5)

    def test_a_scene_needs_its_background_file(self):
        """A clip is never recorded without the background it asks for."""
        scene = [c for c in make_hoeren_audio.all_clips(["A1"]) if c[1].get("scene") == "cafe"][0]
        with mock.patch.object(make_hoeren_audio, "all_clips", return_value=[scene]):
            with mock.patch.object(make_hoeren_audio.llm, "synthesize_speech", return_value=b"x"):
                out = self.run_cmd()
                self.assertIn("needs cafe.mp3", out)
                (self.dir / "cafe.mp3").write_bytes(b"")
                self.run_cmd()
        self.assertTrue((self.dir / f"{scene[0]}.mp3").exists())

    def test_mix_filter(self):
        plain = make_hoeren_audio.mix_filter({})
        self.assertNotIn("amix", plain)
        both = make_hoeren_audio.mix_filter({"scene": "cafe", "gong": True, "phone": True})
        self.assertIn("lowpass=f=3400", both)
        self.assertIn("concat=n=2", both)
        self.assertIn("amix=inputs=2", both)

    def test_stops_at_the_quota(self):
        quota = make_hoeren_audio.llm.AIQuotaError("quota, retry in 13h3m42.3s")
        with mock.patch.object(
            make_hoeren_audio.llm, "synthesize_speech", side_effect=[b"pcm", quota, b"pcm"]
        ) as tts:
            out = self.run_cmd()
        self.assertIn("Quota reached. Try again in 13h3m42s.", out)
        self.assertEqual(tts.call_count, 2)
        self.assertEqual(len(list(self.dir.glob("*.mp3"))), 1)
