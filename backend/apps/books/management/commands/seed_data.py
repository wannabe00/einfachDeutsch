from django.core.management.base import BaseCommand
from django.db import transaction

from apps.books.models import Book, Chapter
from apps.exercises.models import Exercise
from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word

BOOK_TITLE = "Beginner German"


class Command(BaseCommand):
    help = "Seed the database with a sample book, chapters, words, grammar, and exercises."

    @transaction.atomic
    def handle(self, *args, **options):
        if Book.objects.filter(title=BOOK_TITLE).exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Book "{BOOK_TITLE}" already exists — skipping seed (idempotent).'
                )
            )
            return

        book = Book.objects.create(
            title=BOOK_TITLE,
            description="A small starter book for testing the platform.",
        )

        ch1 = Chapter.objects.create(
            book=book,
            number=1,
            title="Greetings",
            description="Basic greetings and polite phrases.",
        )
        ch2 = Chapter.objects.create(
            book=book,
            number=2,
            title="Numbers",
            description="Counting and cardinal numbers.",
        )

        words = [
            (ch1, "hello", "hallo", ""),
            (ch1, "good day", "guten Tag", "Formal daytime greeting."),
            (ch1, "the dog", "der Hund", "Masculine noun."),
            (ch2, "one", "eins", ""),
            (ch2, "the number", "die Zahl", "Feminine noun."),
        ]
        for chapter, english, german, notes in words:
            Word.objects.create(chapter=chapter, english=english, german=german, notes=notes)

        GrammarRule.objects.create(
            chapter=ch1,
            title="The definite article",
            category="articles",
            content=(
                "German has three definite articles: **der** (masculine), "
                "**die** (feminine), and **das** (neuter)."
            ),
            example_sentences="der Hund\ndie Katze\ndas Haus",
        )
        GrammarRule.objects.create(
            chapter=ch2,
            title="Counting from one to three",
            category="other",
            content="The first numbers are `eins`, `zwei`, `drei`.",
            example_sentences="eins, zwei, drei",
        )

        Exercise.objects.create(
            chapter=ch1,
            exercise_type="translation",
            prompt='Translate to German: "hello"',
            correct_answer="hallo",
            hint="It looks a lot like the English word.",
        )
        Exercise.objects.create(
            chapter=ch1,
            exercise_type="article",
            prompt="Choose the correct article: ___ Hund",
            correct_answer="der",
            explanation="Hund is masculine, so it takes der.",
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Seeded "{BOOK_TITLE}": 2 chapters, 5 words, 2 grammar rules, 2 exercises.'
            )
        )
