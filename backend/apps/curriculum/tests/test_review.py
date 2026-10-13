"""Review only covers learned words; the Dashboard reviews the last unit."""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.books.models import Book, Chapter
from apps.curriculum.models import Lesson, PathLessonProgress, Unit
from apps.vocabulary.models import Word


class ReviewScopeTests(TestCase):
    def setUp(self):
        book = Book.objects.create(title="T")
        self.units = []
        for n in (1, 2):
            chapter = Chapter.objects.create(book=book, number=n, title=f"L{n}")
            unit = Unit.objects.create(cefr_level="A1", order=n, title=f"L{n}", chapter=chapter)
            for order in (1, 2):
                lesson = Lesson.objects.create(unit=unit, order=order, title=f"{n}.{order}")
                word = Word.objects.create(
                    chapter=chapter, english=f"w{n}{order}", german=f"Wort{n}{order}"
                )
                lesson.words.add(word)
            self.units.append(unit)

        self.user = get_user_model().objects.create_user("anna", password="pw")
        self.api = APIClient()
        self.api.force_authenticate(self.user)

    def complete(self, unit, order, days_ago=0):
        PathLessonProgress.objects.create(
            user=self.user,
            lesson=unit.lessons.get(order=order),
            completed_at=timezone.now() - timedelta(days=days_ago),
        )

    def due(self):
        return sorted(w["german"] for w in self.api.get("/api/vocabulary/words/due/").json())

    def test_only_learned_words_are_due(self):
        self.assertEqual(self.due(), [])
        self.complete(self.units[0], 1)
        self.assertEqual(self.due(), ["Wort11"])
        counts = self.api.get("/api/vocabulary/words/due-counts/").json()
        self.assertEqual(counts["total"], 1)

    def test_last_unit_needs_a_finished_unit(self):
        self.complete(self.units[0], 1)
        res = self.api.get("/api/vocabulary/words/last-unit/").json()
        self.assertEqual(res, {"unit": None, "words": []})

    def test_last_unit_is_the_most_recently_finished(self):
        self.complete(self.units[0], 1, days_ago=3)
        self.complete(self.units[0], 2, days_ago=3)
        self.complete(self.units[1], 1, days_ago=1)
        self.complete(self.units[1], 2, days_ago=1)
        res = self.api.get("/api/vocabulary/words/last-unit/").json()
        self.assertEqual(res["unit"]["order"], 2)
        self.assertEqual(sorted(w["german"] for w in res["words"]), ["Wort21", "Wort22"])

    def test_dashboard_counts_learned_words(self):
        self.complete(self.units[0], 1)
        stats = self.api.get("/api/stats/").json()
        self.assertEqual((stats["words_learned"], stats["due_today"]), (1, 1))
