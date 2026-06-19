from django.core.management.base import BaseCommand
from django.db import transaction

from apps.books.models import Book, Chapter
from apps.exercises.models import Exercise
from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word

from ._menschen_lessons import EXERCISES, GRAMMAR
from ._menschen_vocab import A1_1_SECTIONS, A1_2_SECTIONS, CHAPTERS, VOCAB

BOOKS = {
    "Menschen A1.1": ("Hueber Menschen A1.1 — Lektionen 1–12.", A1_1_SECTIONS),
    "Menschen A1.2": ("Hueber Menschen A1.2 — Lektionen 13–16.", A1_2_SECTIONS),
}
DEMO_BOOK = "Beginner German"


class Command(BaseCommand):
    help = "Seed the two Menschen A1 books with vocabulary, grammar, and exercises (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete and recreate the Menschen books even if they already exist.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        existing = Book.objects.filter(title__in=BOOKS.keys())
        if existing.exists() and not options["reset"]:
            self.stdout.write(
                self.style.WARNING(
                    "Menschen books already exist — pass --reset to rebuild. Skipping."
                )
            )
            return

        # Remove the demo sample book so it doesn't clutter the real content.
        Book.objects.filter(title=DEMO_BOOK).delete()
        existing.delete()

        totals = {"chapters": 0, "words": 0, "grammar": 0, "exercises": 0}

        for title, (description, sections) in BOOKS.items():
            book = Book.objects.create(title=title, description=description)

            for sec in sections:
                ch_title, ch_desc = CHAPTERS[sec]
                chapter = Chapter.objects.create(
                    book=book, number=sec, title=ch_title, description=ch_desc
                )
                totals["chapters"] += 1

                for german, english in VOCAB.get(sec, []):
                    Word.objects.create(chapter=chapter, english=english, german=german, notes="")
                    totals["words"] += 1

                for g in GRAMMAR.get(sec, []):
                    GrammarRule.objects.create(
                        chapter=chapter,
                        title=g["title"],
                        category=g["category"],
                        content=g["content"],
                        example_sentences=g["examples"],
                    )
                    totals["grammar"] += 1

                for e in EXERCISES.get(sec, []):
                    Exercise.objects.create(
                        chapter=chapter,
                        exercise_type=e["type"],
                        prompt=e["prompt"],
                        correct_answer=e["answer"],
                        hint=e["hint"],
                        explanation=e["explanation"],
                    )
                    totals["exercises"] += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded Menschen A1.1 + A1.2: "
                f"{totals['chapters']} chapters, {totals['words']} words, "
                f"{totals['grammar']} grammar rules, {totals['exercises']} exercises."
            )
        )
