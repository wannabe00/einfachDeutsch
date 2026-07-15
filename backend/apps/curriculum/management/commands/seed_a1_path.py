"""Seed the A1 learning path from `a1_curriculum.py` (Phase 23.3).

Idempotent: re-running updates the same rows (keyed by natural keys / a stable
`source` per exercise), so it's safe to run locally and on Neon. Content is
original (authored to Menschen A1 themes, not copied).

    python manage.py seed_a1_path

Creates: a Book "einfachDeutsch — A1" with one Chapter per Unit, the unit's
Words / GrammarRules / Exercises, and the path Units → Lessons → LessonItems.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.books.models import Book, Chapter
from apps.curriculum.a1_curriculum import A1_LEVEL, A1_UNITS
from apps.curriculum.models import Lesson, LessonItem, Unit
from apps.exercises.models import Exercise
from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word

BOOK_TITLE = "einfachDeutsch — A1"
SIMPLE_TYPES = {"translation", "fill_blank", "article", "conjugation", "free_text"}


class Command(BaseCommand):
    help = "Seed the original A1 learning path (idempotent)."

    def handle(self, *args, **options):
        counts = {"units": 0, "lessons": 0, "items": 0, "words": 0, "grammar": 0, "exercises": 0}

        with transaction.atomic():
            book, _ = Book.objects.get_or_create(
                title=BOOK_TITLE,
                defaults={"description": "Original A1 curriculum for the learning path."},
            )

            for u in A1_UNITS:
                chapter, _ = Chapter.objects.update_or_create(
                    book=book,
                    number=u["order"],
                    defaults={"title": u["title"], "description": u.get("theme", "")},
                )

                words = {}
                for english, german in u["words"]:
                    word, _ = Word.objects.update_or_create(
                        chapter=chapter, german=german, defaults={"english": english}
                    )
                    words[german] = word
                    counts["words"] += 1

                rules = {}
                for g in u.get("grammar", []):
                    rule, _ = GrammarRule.objects.update_or_create(
                        chapter=chapter,
                        title=g["title"],
                        defaults={
                            "category": g["category"],
                            "content": g["content"],
                            "example_sentences": g.get("examples", ""),
                        },
                    )
                    rules[g["title"]] = rule
                    counts["grammar"] += 1

                unit, _ = Unit.objects.update_or_create(
                    cefr_level=A1_LEVEL,
                    order=u["order"],
                    defaults={
                        "title": u["title"],
                        "theme": u.get("theme", ""),
                        "accent_color": u.get("accent_color", ""),
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
                            source = f"seed-a1-u{u['order']}-l{lspec['order']}-{idx}"
                            defaults["exercise"] = self._upsert_exercise(chapter, source, item)
                            counts["exercises"] += 1
                        elif item["kind"] == "review":
                            defaults["word"] = words[item["word"]]
                        elif item["kind"] == "grammar":
                            defaults["grammar_rule"] = rules[item["grammar"]]

                        LessonItem.objects.update_or_create(
                            lesson=lesson, order=idx, defaults=defaults
                        )
                        counts["items"] += 1

        self.stdout.write(self.style.SUCCESS("Seeded A1 learning path:"))
        for k, v in counts.items():
            self.stdout.write(f"  {k}: {v}")

    def _upsert_exercise(self, chapter, source, item) -> Exercise:
        etype = item["type"]
        defaults = {
            "chapter": chapter,
            "exercise_type": etype,
            "prompt": item["prompt"],
            "hint": item.get("hint", ""),
            "explanation": item.get("explanation", ""),
        }
        if etype == "multiple_choice":
            defaults["payload"] = {"options": item["options"], "answer": item["answer"]}
            defaults["correct_answer"] = ""
        elif etype == "sentence_order":
            defaults["payload"] = {"tokens": item["tokens"], "answer": item["answer"]}
            defaults["correct_answer"] = ""
        else:  # simple text-answer types
            defaults["payload"] = {}
            defaults["correct_answer"] = item["answer"]

        exercise, _ = Exercise.objects.update_or_create(source=source, defaults=defaults)
        return exercise
