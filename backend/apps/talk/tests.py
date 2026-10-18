"""Talk to AI: the Live token, the report and the history."""

from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.ai_assistant import llm
from apps.curriculum.models import PathLessonProgress, Unit

from .models import Talk

REPORT = {
    "summary": "Gut gemacht!",
    "corrections": [
        {"you_said": "Ich bin 20 Jahre.", "better": "Ich bin 20 Jahre alt.", "why": "Add alt."}
    ],
    "phrases": ["Ich hätte gern …"],
    "new_words": [{"german": "die Speisekarte", "english": "menu"}],
    "practise": ["Numbers"],
}


class TalkTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_path", stdout=StringIO())

    def setUp(self):
        cache.clear()  # AI throttle counters
        self.user = get_user_model().objects.create_user("anna", password="pw")
        self.user.profile.is_premium = True
        self.user.profile.save()
        self.api = APIClient()
        self.api.force_authenticate(self.user)
        self.token = self.enterContext(mock.patch.object(llm, "live_token", return_value="tok"))

    def finish_modul_1(self):
        for unit in Unit.objects.filter(cefr_level="A1", order__in=(1, 2, 3)):
            for lesson in unit.lessons.all():
                PathLessonProgress.objects.create(
                    user=self.user, lesson=lesson, completed_at=timezone.now()
                )

    def start(self):
        return self.api.post("/api/talk/start/", {}, format="json")

    def test_free_users_are_turned_away(self):
        self.user.profile.is_premium = False
        self.user.profile.save()
        self.assertEqual(self.start().status_code, 403)
        self.assertEqual(self.api.get("/api/talk/").status_code, 403)

    def test_start_locks_level_opener_and_topics_into_the_token(self):
        self.finish_modul_1()
        res = self.start().json()
        self.assertEqual((res["token"], res["model"]), ("tok", llm.LIVE_MODEL))
        instruction = self.token.call_args[0][0]
        self.assertIn(llm.TALK_LEVEL["A1"], instruction)
        self.assertIn("sehr langsam", instruction)
        self.assertIn(llm.TALK_GREETING, instruction)  # Tako always greets first
        self.assertTrue(any(o in instruction for o in llm.TALK_OPENERS))
        self.assertIn("Familie und Sprachen", instruction)  # a finished Lektion's theme
        self.assertNotIn("Möbel und Preise", instruction)  # Lektion 4 isn't finished

    def test_the_ai_speaks_at_the_users_level(self):
        self.user.profile.cefr_level = "B1"
        self.user.profile.save()
        self.start()
        instruction = self.token.call_args[0][0]
        self.assertIn(llm.TALK_LEVEL["B1"], instruction)
        self.assertNotIn(llm.TALK_LEVEL["A1"], instruction)

    @override_settings(TALK_DAILY_CAP=2)
    def test_daily_cap(self):
        self.assertEqual(self.start().status_code, 200)
        self.assertEqual(self.start().status_code, 200)
        self.assertEqual(self.start().status_code, 429)

    def test_ai_errors_create_no_talk(self):
        self.token.side_effect = llm.AIResponseError("busy")
        self.assertEqual(self.start().status_code, 502)
        self.token.side_effect = llm.AIConfigError("no key")
        self.assertEqual(self.start().status_code, 503)
        self.assertEqual(Talk.objects.count(), 0)

    def test_finish_saves_the_transcript_and_report(self):
        talk_id = self.start().json()["id"]
        url = f"/api/talk/{talk_id}/finish/"
        self.assertEqual(self.api.post(url, {"transcript": "nope"}, format="json").status_code, 400)
        transcript = [
            {"role": "ai", "text": "Hallo! Wie geht's dir heute?"},
            {"role": "user", "text": "Gut. Ich bin 20 Jahre." + "x" * 1000},
            {"role": "user", "text": "   "},
            {"role": "user", "text": "Ich bin مرحبا"},
            {"role": "user", "text": "Sorry, I don't know. Café?"},
        ]
        with mock.patch.object(llm, "talk_report", side_effect=llm.AIResponseError("busy")):
            self.assertEqual(
                self.api.post(url, {"transcript": transcript}, format="json").status_code, 502
            )
        with mock.patch.object(llm, "talk_report", return_value=REPORT):  # retry works
            data = self.api.post(url, {"transcript": transcript}, format="json").json()
        self.assertEqual(data["report"], REPORT)
        talk = Talk.objects.get()
        self.assertEqual(len(talk.transcript), 4)  # the empty line is dropped
        self.assertEqual(len(talk.transcript[1]["text"]), 600)  # capped
        self.assertEqual(talk.transcript[2]["text"], "(unklar)")  # not German or English
        self.assertEqual(talk.transcript[3]["text"], "Sorry, I don't know. Café?")  # English stays
        self.assertEqual(
            self.api.post(url, {"transcript": transcript}, format="json").status_code, 400
        )

    def test_history_is_private(self):
        talk_id = self.start().json()["id"]
        with mock.patch.object(llm, "talk_report", return_value=REPORT):
            self.api.post(
                f"/api/talk/{talk_id}/finish/",
                {"transcript": [{"role": "user", "text": "Hallo"}]},
                format="json",
            )
        self.assertEqual(self.api.get("/api/talk/").json()[0]["summary"], "Gut gemacht!")
        other = get_user_model().objects.create_user("ben", password="pw")
        other.profile.is_premium = True
        other.profile.save()
        api = APIClient()
        api.force_authenticate(other)
        self.assertEqual(api.get("/api/talk/").json(), [])
        self.assertEqual(api.get(f"/api/talk/{talk_id}/").status_code, 404)

    def test_recite_is_gone(self):
        self.assertEqual(self.api.post("/api/recite/").status_code, 404)

    def test_removing_wipes_the_text_but_keeps_the_cap(self):
        ids = []
        for _ in range(2):
            talk_id = self.start().json()["id"]
            with mock.patch.object(llm, "talk_report", return_value=REPORT):
                self.api.post(
                    f"/api/talk/{talk_id}/finish/",
                    {"transcript": [{"role": "user", "text": "Hallo"}]},
                    format="json",
                )
            ids.append(talk_id)
        other = Talk.objects.create(user=get_user_model().objects.create_user("ben"), level="A1")
        self.assertEqual(
            self.api.post("/api/talk/remove/", {"ids": "x"}, format="json").status_code, 400
        )
        res = self.api.post("/api/talk/remove/", {"ids": [*ids, other.id]}, format="json").json()
        self.assertEqual(res["removed"], 2)  # never someone else's
        self.assertEqual(self.api.get("/api/talk/").json(), [])
        self.assertEqual(self.api.get(f"/api/talk/{ids[0]}/").status_code, 404)
        gone = Talk.objects.get(id=ids[0])
        self.assertEqual((gone.transcript, gone.report), ([], {}))
        with override_settings(TALK_DAILY_CAP=2):
            self.assertEqual(self.start().status_code, 429)  # removed talks still count
