"""The Grundlagen starter units (A0): optional, always open, free of energy."""

import base64

from apps.books.models import Book, Chapter
from apps.curriculum.content.dsl import dictate, hear
from apps.curriculum.grading import public_exercise
from apps.curriculum.management.commands.seed_path import exercise_fields
from apps.curriculum.models import EnergyState, Lesson, LessonItem, Unit
from apps.exercises.models import Exercise

from .test_multipart import LessonFixture


class StarterTests(LessonFixture):
    def setUp(self):
        super().setUp()
        self.user.profile.is_premium = False
        self.user.profile.save()
        EnergyState.objects.update_or_create(user=self.user, defaults={"balance": 0})

        chapter = Chapter.objects.create(book=Book.objects.create(title="S"), number=1, title="G")
        unit = Unit.objects.create(cefr_level="A0", order=1, title="Grundlagen", chapter=chapter)
        self.starter = Lesson.objects.create(unit=unit, order=1, title="Alphabet")
        self.hear = Exercise.objects.create(
            chapter=chapter, **exercise_fields(hear("drei", "3", "2", "8"))
        )
        self.spell = Exercise.objects.create(
            chapter=chapter, **exercise_fields(dictate("Max", say="M. A. X."))
        )
        self.hear_item = LessonItem.objects.create(lesson=self.starter, order=0, exercise=self.hear)
        self.spell_item = LessonItem.objects.create(
            lesson=self.starter, order=1, exercise=self.spell
        )

    def test_shown_first_and_open_but_never_next_up(self):
        data = self.api.get("/api/curriculum/path/").json()
        self.assertEqual(data["units"][0]["cefr_level"], "A0")
        self.assertNotEqual(data["units"][0]["lessons"][0]["state"], "locked")
        self.assertEqual(data["next_up"]["lesson_id"], self.lesson.id)

    def test_free_without_energy(self):
        url = f"/api/curriculum/lessons/{self.starter.id}/"
        items = self.api.get(url).json()["items"]
        payloads = [i["content"]["payload"] for i in items]
        self.assertIn("say", payloads[0])  # "what do you hear?" gets a Listen button
        self.assertNotIn("answer", str(payloads))
        answers = [
            {"item_id": self.hear_item.id, "answer": "3"},
            {"item_id": self.spell_item.id, "answer": "max"},
        ]
        res = self.api.post(f"{url}complete/", {"answers": answers}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(EnergyState.objects.get(user=self.user).balance, 0)
        # A real A1 lesson still needs energy.
        self.assertEqual(self.api.get(self.url()).status_code, 402)

    def test_spelling_reads_the_letters_not_the_word(self):
        say = public_exercise(self.spell)["payload"]["say"]
        self.assertEqual(base64.b64decode(say).decode(), "M. A. X.")
