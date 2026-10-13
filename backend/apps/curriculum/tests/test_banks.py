"""Word Bank and Grammar list only what the user has learned."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.books.models import Book, Chapter
from apps.curriculum.models import Lesson, LessonItem, PathLessonProgress, Unit
from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word


class BankTests(TestCase):
    def setUp(self):
        chapter = Chapter.objects.create(book=Book.objects.create(title="T"), number=1, title="L1")
        unit = Unit.objects.create(cefr_level="A1", order=1, title="Hallo", chapter=chapter)
        self.words = Lesson.objects.create(unit=unit, order=1, title="Wortschatz")
        self.rules = Lesson.objects.create(unit=unit, order=2, title="Grammatik")
        hund = Word.objects.create(
            chapter=chapter, english="dog", german="der Hund", notes="Pl. die Hunde"
        )
        Word.objects.create(chapter=chapter, english="cat", german="die Katze")
        self.words.words.add(hund)
        self.rules.words.add(Word.objects.get(german="die Katze"))
        self.rule = GrammarRule.objects.create(chapter=chapter, title="sein")
        LessonItem.objects.create(
            lesson=self.rules, order=0, kind="grammar", grammar_rule=self.rule
        )

        self.user = get_user_model().objects.create_user("anna", password="pw")
        self.api = APIClient()
        self.api.force_authenticate(self.user)

    def complete(self, lesson):
        PathLessonProgress.objects.create(
            user=self.user, lesson=lesson, completed_at=timezone.now()
        )

    def test_word_bank_lists_learned_words_with_topic_and_plural(self):
        self.complete(self.words)
        words = self.api.get("/api/vocabulary/words/").json()
        self.assertEqual([w["german"] for w in words], ["der Hund"])
        self.assertEqual(words[0]["plural"], "die Hunde")
        self.assertEqual(words[0]["topic"]["title"], "Hallo")

    def test_grammar_lists_learned_topics_and_teases_the_next(self):
        self.assertEqual(self.api.get("/api/grammar/rules/").json(), [])
        nxt = self.api.get("/api/grammar/rules/next/").json()["next"]
        self.assertEqual((nxt["title"], nxt["lesson"]["title"]), ("sein", "Grammatik"))

        self.complete(self.rules)
        self.assertEqual([r["title"] for r in self.api.get("/api/grammar/rules/").json()], ["sein"])
        self.assertIsNone(self.api.get("/api/grammar/rules/next/").json()["next"])
