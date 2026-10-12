"""Seed the A1 learning path from `apps/curriculum/content/a1`.

    python manage.py seed_a1_path

Builds the book "einfachDeutsch — A1" with one chapter per unit (Lektion),
each holding the unit's words, grammar and exercises, plus the path itself:
units, lessons and lesson items.

Safe to re-run. Rows are matched on natural keys (and a stable `source` for
exercises), so a second run updates rather than duplicates. Anything an earlier
run created that the content no longer contains is deleted, so editing the
content files and re-seeding leaves no leftovers.

It also removes the old "Menschen A1.1" / "Menschen A1.2" books, which this
content replaces.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.books.models import Book, Chapter
from apps.curriculum.content.a1 import A1_LEVEL, A1_UNITS
from apps.curriculum.models import Lesson, LessonItem, Unit
from apps.exercises.models import Exercise
from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word

BOOK_TITLE = "einfachDeutsch — A1"
SOURCE_PREFIX = "seed-a1-"
LEGACY_BOOKS = ("Menschen A1.1", "Menschen A1.2")


def exercise_fields(item: dict) -> dict:
    """The Exercise fields for one exercise item from the content files."""
    etype = item["type"]
    fields = {
        "exercise_type": etype,
        "prompt": item["prompt"],
        "hint": item.get("hint", ""),
        "explanation": item.get("explanation", ""),
        "correct_answer": "",
    }
    if etype == "multiple_choice":
        fields["payload"] = {"options": item["options"], "answer": item["answer"]}
    elif etype == "sentence_order":
        fields["payload"] = {"tokens": item["tokens"], "answer": item["answer"]}
    elif etype == "word_bank":
        fields["payload"] = {
            "text": item["text"],
            "bank": item["bank"],
            "answers": item["answers"],
        }
    elif etype == "matching":
        fields["payload"] = {"pairs": item["pairs"]}
    else:  # translation, fill_blank, article, conjugation
        fields["payload"] = {}
        fields["correct_answer"] = item["answer"]
    return fields


def word_fields(word: tuple) -> tuple[str, dict]:
    """(german, defaults) for a `(english, german, pos[, notes])` tuple."""
    english, german, part_of_speech, *rest = word
    return german, {
        "english": english,
        "part_of_speech": part_of_speech,
        "notes": rest[0] if rest else "",
    }


class Command(BaseCommand):
    help = "Seed the A1 learning path. Safe to re-run."

    def handle(self, *args, **options):
        counts = dict.fromkeys(
            ["units", "lessons", "items", "words", "grammar", "exercises", "removed"], 0
        )

        with transaction.atomic():
            legacy = Book.objects.filter(title__in=LEGACY_BOOKS)
            if legacy.exists():
                self.stdout.write(f"Removing old books: {', '.join(b.title for b in legacy)}")
                legacy.delete()

            book, _ = Book.objects.get_or_create(
                title=BOOK_TITLE,
                defaults={"description": "The A1 learning path."},
            )

            for u in A1_UNITS:
                self._seed_unit(book, u, counts)

            self._remove_leftovers(book, counts)

        self.stdout.write(self.style.SUCCESS("Seeded the A1 learning path:"))
        for k, v in counts.items():
            self.stdout.write(f"  {k}: {v}")

    def _seed_unit(self, book, u, counts):
        chapter, _ = Chapter.objects.update_or_create(
            book=book,
            number=u["order"],
            defaults={"title": u["title"], "description": u["theme"], "cefr_level": A1_LEVEL},
        )

        words = {}
        for w in u["words"]:
            german, defaults = word_fields(w)
            words[german], _ = Word.objects.update_or_create(
                chapter=chapter, german=german, defaults=defaults
            )
        Word.objects.filter(chapter=chapter).exclude(german__in=words).delete()
        counts["words"] += len(words)

        rules = {}
        for g in u["grammar"]:
            rules[g["title"]], _ = GrammarRule.objects.update_or_create(
                chapter=chapter,
                title=g["title"],
                defaults={
                    "category": g["category"],
                    "content": g["content"],
                    "example_sentences": g["examples"],
                },
            )
        GrammarRule.objects.filter(chapter=chapter).exclude(title__in=rules).delete()
        counts["grammar"] += len(rules)

        unit, _ = Unit.objects.update_or_create(
            cefr_level=A1_LEVEL,
            order=u["order"],
            defaults={
                "title": u["title"],
                "theme": u["theme"],
                "accent_color": u["accent_color"],
                "chapter": chapter,
            },
        )
        counts["units"] += 1

        for lspec in u["lessons"]:
            lesson, _ = Lesson.objects.update_or_create(
                unit=unit,
                order=lspec["order"],
                defaults={"title": lspec["title"], "xp_reward": lspec.get("xp", 10)},
            )
            counts["lessons"] += 1

            for idx, item in enumerate(lspec["items"]):
                defaults = {
                    "kind": item["kind"],
                    "exercise": None,
                    "word": None,
                    "grammar_rule": None,
                }
                if item["kind"] == "exercise":
                    source = f"{SOURCE_PREFIX}u{u['order']}-l{lspec['order']}-{idx}"
                    defaults["exercise"], _ = Exercise.objects.update_or_create(
                        source=source, defaults={"chapter": chapter, **exercise_fields(item)}
                    )
                    counts["exercises"] += 1
                elif item["kind"] == "review":
                    defaults["word"] = words[item["word"]]
                elif item["kind"] == "grammar":
                    defaults["grammar_rule"] = rules[item["grammar"]]
                LessonItem.objects.update_or_create(lesson=lesson, order=idx, defaults=defaults)
                counts["items"] += 1

            LessonItem.objects.filter(lesson=lesson, order__gte=len(lspec["items"])).delete()

        unit.lessons.filter(order__gt=len(u["lessons"])).delete()

    def _remove_leftovers(self, book, counts):
        """Delete what earlier runs created but the content no longer has."""

        def remove(qs):
            counts["removed"] += qs.count()
            qs.delete()

        remove(Unit.objects.filter(cefr_level=A1_LEVEL, order__gt=len(A1_UNITS)))
        remove(Chapter.objects.filter(book=book, number__gt=len(A1_UNITS)))
        # Only after units and lessons are gone do we know which exercises are unused.
        used = set(
            LessonItem.objects.filter(exercise__isnull=False).values_list(
                "exercise__source", flat=True
            )
        )
        remove(Exercise.objects.filter(source__startswith=SOURCE_PREFIX).exclude(source__in=used))
