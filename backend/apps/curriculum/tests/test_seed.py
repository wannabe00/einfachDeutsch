"""The seed command against a real (test) database."""

import io

from django.core.management import call_command
from django.db import connection
from django.test import TestCase

from apps.books.models import Book, Chapter
from apps.curriculum.content.a1 import A1_UNITS
from apps.curriculum.models import Lesson, LessonItem, Unit
from apps.exercises.models import Exercise
from apps.vocabulary.models import Word

# A run against Neon pays a network round trip per query, so keep it small.
MAX_QUERIES = 600


def seed():
    calls = [0]

    def count(execute, sql, params, many, context):
        calls[0] += 1
        return execute(sql, params, many, context)

    with connection.execute_wrapper(count):
        call_command("seed_a1_path", stdout=io.StringIO())
    return calls[0]


def snapshot():
    return {
        "units": Unit.objects.count(),
        "lessons": Lesson.objects.count(),
        "items": LessonItem.objects.count(),
        "exercises": Exercise.objects.count(),
        "words": Word.objects.count(),
        "item_rows": sorted(
            LessonItem.objects.values_list(
                "lesson_id", "order", "kind", "exercise_id", "word_id", "grammar_rule_id"
            )
        ),
    }


class SeedTests(TestCase):
    def test_fresh_seed_builds_everything_and_removes_legacy_books(self):
        old = Book.objects.create(title="Menschen A1.1")
        chapter = Chapter.objects.create(book=old, number=1, title="Lektion 1")
        Word.objects.create(chapter=chapter, english="dog", german="der Hund")

        queries = seed()

        self.assertFalse(Book.objects.filter(title="Menschen A1.1").exists())
        expected_items = sum(len(les["items"]) for u in A1_UNITS for les in u["lessons"])
        self.assertEqual(Unit.objects.filter(cefr_level="A1").count(), len(A1_UNITS))
        self.assertEqual(LessonItem.objects.count(), expected_items)
        self.assertLessEqual(queries, MAX_QUERIES)

    def test_second_run_changes_nothing_and_is_cheap(self):
        seed()
        before = snapshot()
        queries = seed()
        self.assertEqual(snapshot(), before)
        self.assertLessEqual(queries, MAX_QUERIES)

    def test_every_lesson_item_points_at_exactly_one_thing(self):
        seed()
        for item in LessonItem.objects.all():
            refs = [item.exercise_id, item.word_id, item.grammar_rule_id]
            self.assertEqual(sum(r is not None for r in refs), 1, item)
