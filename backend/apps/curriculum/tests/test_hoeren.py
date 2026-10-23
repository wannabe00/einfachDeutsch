"""Hören: exam-style listening sets, their audio manifest and the generator."""

import json
import tempfile
from io import StringIO
from pathlib import Path
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
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


# A2 like Goethe A2: Teil 2 and 4 are one recording for the whole Teil.
A2_SHAPE = [(5, 2), (5, 1), (5, 1), (5, 2)]


def _plays(teil):
    return (teil.get("clip") or teil["parts"][0]["clip"])["plays"]


# B1 like Goethe B1: five short texts (2 questions, twice), a talk (5, once), a
# conversation (7, once) and a discussion with three voices (8, twice).
B1_SHAPE = [(2, 2)] * 5 + [(5, 1), (7, 1), (8, 2)]


class ContentTests(TestCase):
    def test_b1_sets_have_the_exam_shape(self):
        for modul, teile in LEVELS["B1"]["hoeren"].items():
            where = f"B1 Modul {modul}"
            self.assertEqual([(len(t["parts"]), _plays(t)) for t in teile], B1_SHAPE, where)
            self.assertEqual(sum(len(t["parts"]) for t in teile), 30, where)
            for teil in teile:
                for part in teil["parts"]:
                    self.assertIn(part["answer"], part["options"], where)
            for teil in teile[5:]:
                self.assertGreater(len({p["answer"] for p in teil["parts"]}), 1, where)
            speakers = {who for who, _ in teile[7]["clip"]["script"]}
            self.assertEqual(len(speakers), 3, where)  # host and two guests
            self.assertTrue(teile[7]["clip"]["radio"], where)

    def test_a2_sets_have_the_exam_shape(self):
        for modul, teile in LEVELS["A2"]["hoeren"].items():
            where = f"A2 Modul {modul}"
            self.assertEqual([(len(t["parts"]), _plays(t)) for t in teile], A2_SHAPE, where)
            for teil in teile:
                self.assertGreater(len({p["answer"] for p in teil["parts"]}), 1, where)
                for part in teil["parts"]:
                    self.assertIn(part["answer"], part["options"], where)
            self.assertTrue(teile[1]["context"] and teile[1]["clip"], where)  # choices + one talk
            self.assertTrue(teile[3]["clip"]["radio"], where)  # a radio interview
            for part in teile[0]["parts"]:  # phone, loudspeaker or radio, never plain
                kinds = [k for k in ("phone", "gong", "radio") if part["clip"].get(k)]
                self.assertEqual(len(kinds), 1, f"{where}: {part['prompt']}")

    def test_a1_sets_have_the_exam_shape(self):
        spec = LEVELS["A1"]
        sets = [(f"A1 Modul {m}", t) for m, t in spec["hoeren"].items()]
        sets += [(f"A1 Modul {m} (next)", t) for m, t in spec["hoeren_next"].items()]
        for where, teile in sets:
            self.assertEqual([(len(t["parts"]), _plays(t)) for t in teile], A1_SHAPE, where)
            self.assertTrue(teile[0]["clip"] and teile[2]["clip"]["phone"], where)  # long ones
            for teil in teile:
                answers = {p["answer"] for p in teil["parts"]}
                self.assertGreater(len(answers), 1, f"{where}: {teil['prompt']}")
                for part in teil["parts"]:
                    self.assertIn(part["answer"], part["options"], where)

    def test_clip_names_are_unique(self):
        names = [n for n, _, _ in make_hoeren_audio.all_clips(list(LEVELS))]
        self.assertEqual(len(names), len(set(names)))


class HoerenFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_path", stdout=StringIO())

    def setUp(self):
        self.user = get_user_model().objects.create_user("anna", password="pw")
        self.user.profile.is_premium = True  # the skills are premium
        self.user.profile.save()
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
        self.assertNotIn("noch frei", dumped.split('"options"')[0])  # no script before options
        self.assertNotIn('"script"', dumped)
        self.assertNotIn('"answer"', dumped)
        whole = data["teile"][0]["payload"]["audio"]  # Teil 1: one recording for all
        first = hoeren.clips_of(self.teile[0])[0][0]
        self.assertEqual(whole, {"url": f"/hoeren/{first}.mp3", "plays": 2})
        self.assertEqual(data["teile"][1]["payload"]["parts"][0]["payload"]["audio"]["plays"], 1)

    def test_answer_reveals_transcripts(self):
        teil = self.teile[0]
        right = [p["answer"] for p in teil.payload["parts"]]
        with self.recorded:
            res = self.api.post(f"{BASE}/teil/{teil.id}/answer/", {"answer": right}, format="json")
        data = res.json()
        self.assertEqual(data["parts"], [True] * 5)
        self.assertEqual(len(data["transcripts"]), 1)  # one conversation
        self.assertEqual(len(self.teile), 3)
        self.assertIn("Mann: Hallo! Ist hier noch frei?", data["transcripts"][0])


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
        for name, clip, _ in make_hoeren_audio.all_clips(list(LEVELS)):
            for f in make_hoeren_audio.sound_files(clip, name):
                f.touch()  # the background sounds, so no clip is skipped
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

    def test_several_versions_of_a_sound(self):
        files = make_hoeren_audio.sound_files
        rec = {"script": [["Frau", "x"]], "scene": "cafe"}
        self.assertEqual(files(rec, "a")[0].name, "cafe.mp3")  # none yet: reported missing
        for n in ("cafe.mp3", "cafe-2.mp3", "cafe-3.mp3"):
            (self.dir / n).write_bytes(b"")
        picked = {files(rec, f"clip-{i}")[0].name for i in range(30)}
        self.assertEqual(picked, {"cafe.mp3", "cafe-2.mp3", "cafe-3.mp3"})  # they vary
        self.assertEqual(files(rec, "clip-7"), files(rec, "clip-7"))  # but stay fixed per clip

    def test_mix_filter(self):
        mix = make_hoeren_audio.mix_filter
        self.assertNotIn("amix", mix({"script": [["Frau", "x"]]}))
        call = mix({"script": [["Frau", "x"], ["Mann", "y"]], "phone": True})
        self.assertIn("425*t", call)  # the German ring tone
        self.assertIn("lowpass=f=3400", call)  # thin like a phone
        self.assertNotIn("1000*t", call)  # no beep: someone answers
        self.assertIn("1000*t", mix({"script": [["Frau", "x"]], "phone": True}))  # voicemail
        pa = mix({"script": [["Ansage", "x"]], "gong": True, "scene": "bahnhof"})
        self.assertIn("aecho", pa)  # loudspeaker
        self.assertIn("concat=n=2", pa)  # gong, then the voice
        self.assertIn("amix=inputs=2", pa)  # over the station
        self.assertIn("highpass=f=120", mix({"script": [["Ansage", "x"]], "radio": True}))

    def test_stops_at_the_quota(self):
        quota = make_hoeren_audio.llm.AIQuotaError("quota, retry in 13h3m42.3s")
        with mock.patch.object(
            make_hoeren_audio.llm, "synthesize_speech", side_effect=[b"pcm", quota, b"pcm"]
        ) as tts:
            out = self.run_cmd()
        self.assertIn("Quota reached. Try again in 13h3m42s.", out)
        self.assertEqual(tts.call_count, 2)
        self.assertEqual(len(list(self.dir.glob("*.mp3"))), 1)

    @override_settings(AZURE_SPEECH_KEY="k", AZURE_SPEECH_REGION="westeurope")
    def test_azure_speaks_when_configured(self):
        llm = make_hoeren_audio.llm
        ok = mock.Mock(status_code=200, content=b"pcm")
        with mock.patch.object(llm.httpx, "post", return_value=ok) as post:
            pcm = llm.synthesize_speech([("Frau", "Hallo & tschüss"), ("Mann", "Ja.")], slow=True)
        self.assertEqual(pcm, b"pcm")
        ssml = post.call_args.kwargs["content"].decode()
        self.assertIn("de-DE-SeraphinaMultilingualNeural", ssml)
        self.assertIn("de-DE-FlorianMultilingualNeural", ssml)
        self.assertIn("Hallo &amp; tschüss", ssml)
        self.assertIn('rate="-15%"', ssml)
        self.assertIn("westeurope", post.call_args.args[0])
        with mock.patch.object(llm.httpx, "post", return_value=mock.Mock(status_code=429)):
            with self.assertRaises(llm.AIQuotaError):
                llm.synthesize_speech([("Ansage", "Achtung")])
