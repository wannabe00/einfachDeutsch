"""Which words and grammar topics count as learned."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.books.models import Book, Chapter
from apps.curriculum.learned import learned_rule_ids, learned_word_ids
from apps.curriculum.models import Lesson, LessonItem, PathLessonProgress, Unit
from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word


def make_unit(book, level, order):
    number = Chapter.objects.filter(book=book).count() + 1
    chapter = Chapter.objects.create(book=book, number=number, title=f"L{order}", cefr_level=level)
    unit = Unit.objects.create(cefr_level=level, order=order, title=f"L{order}", chapter=chapter)
    first = Lesson.objects.create(unit=unit, order=1, title="one")
    second = Lesson.objects.create(unit=unit, order=2, title="two")
    return chapter, first, second


class LearnedTests(TestCase):
    def setUp(self):
        book = Book.objects.create(title="Test")
        self.chapter, self.first, self.second = make_unit(book, "A1", 1)
        self.hund = Word.objects.create(chapter=self.chapter, english="dog", german="der Hund")
        self.katze = Word.objects.create(chapter=self.chapter, english="cat", german="die Katze")
        self.first.words.add(self.hund)
        self.second.words.add(self.katze)
        self.rule = GrammarRule.objects.create(chapter=self.chapter, title="Artikel")
        LessonItem.objects.create(
            lesson=self.second, order=0, kind="grammar", grammar_rule=self.rule
        )
        a2_chapter, a2_lesson, _ = make_unit(book, "A2", 1)
        self.a2_word = Word.objects.create(chapter=a2_chapter, english="tree", german="der Baum")
        a2_lesson.words.add(self.a2_word)
        self.user = get_user_model().objects.create_user("anna", password="pw")

    def complete(self, lesson):
        PathLessonProgress.objects.create(
            user=self.user, lesson=lesson, completed_at=timezone.now()
        )

    def test_nothing_is_learned_before_any_lesson(self):
        self.assertEqual(learned_word_ids(self.user), set())
        self.assertEqual(learned_rule_ids(self.user), set())

    def test_finishing_a_lesson_teaches_only_its_words(self):
        self.complete(self.first)
        self.assertEqual(learned_word_ids(self.user), {self.hund.id})
        self.assertEqual(learned_rule_ids(self.user), set())

        self.complete(self.second)
        self.assertEqual(learned_word_ids(self.user), {self.hund.id, self.katze.id})
        self.assertEqual(learned_rule_ids(self.user), {self.rule.id})

    def test_levels_below_count_as_learned_and_above_never(self):
        self.user.profile.cefr_level = "A2"
        self.user.profile.save()
        self.assertEqual(learned_word_ids(self.user), {self.hund.id, self.katze.id})

        self.user.profile.cefr_level = "A1"
        self.user.profile.save()
        PathLessonProgress.objects.create(
            user=self.user, lesson=self.a2_word.taught_in.get(), completed_at=timezone.now()
        )
        self.assertNotIn(self.a2_word.id, learned_word_ids(self.user))

    def test_words_no_lesson_teaches_are_learned(self):
        own = Word.objects.create(chapter=self.chapter, english="house", german="das Haus")
        self.assertEqual(learned_word_ids(self.user), {own.id})

    def test_guests_learn_nothing(self):
        from django.contrib.auth.models import AnonymousUser

        self.assertEqual(learned_word_ids(AnonymousUser()), set())
