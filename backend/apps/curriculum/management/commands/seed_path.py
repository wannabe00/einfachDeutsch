"""Seed the learning path of every level from `apps/curriculum/content`.

    python manage.py seed_path            # every level
    python manage.py seed_path --level A2 # one level

For each level, builds the book "einfachDeutsch — <level>" with one chapter
per unit (Lektion), each holding the unit's words, grammar and exercises, plus
the path itself: units, lessons and lesson items, and the checks' exercises.

Safe to re-run. Rows are matched on natural keys (and a stable `source` for
exercises): existing rows are updated, missing ones created, and rows the
content no longer has are deleted, so editing the content and re-seeding
leaves no leftovers. It also removes the old "Menschen A1.1" / "Menschen A1.2"
books, which this content replaces.

The work is done in bulk: existing rows are read once per table, compared in
Python, and only real changes are written, in batches. Against a remote
database (Neon) that is a few hundred queries instead of tens of thousands.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.books.models import Book, Chapter
from apps.curriculum.checks import MODUL_SIZE, check_source
from apps.curriculum.content.levels import LEVELS
from apps.curriculum.models import Lesson, LessonItem, Unit
from apps.exercises.models import Exercise
from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word

LEGACY_BOOKS = ("Menschen A1.1", "Menschen A1.2")


def book_title(level: str) -> str:
    return f"einfachDeutsch — {level}"


def source_prefix(level: str) -> str:
    return f"seed-{level.lower()}-"


BATCH = 500


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
    elif etype == "error_spot":
        fields["payload"] = {
            "tokens": item["tokens"],
            "answer": item["answer"],
            "correction": item["correction"],
        }
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
    elif etype == "group":
        fields["payload"] = {
            "parts": [{k: v for k, v in p.items() if k != "kind"} for p in item["parts"]]
        }
    else:  # translation, fill_blank, article, conjugation, dictation
        fields["payload"] = {}
        fields["correct_answer"] = item["answer"]
    if item.get("context"):  # a dialogue or reading text shown above the task
        fields["payload"]["context"] = item["context"]
    return fields


def word_fields(word: tuple) -> tuple[str, dict]:
    """(german, fields) for a `(english, german, pos[, notes])` tuple."""
    english, german, part_of_speech, *rest = word
    return german, {
        "english": english,
        "part_of_speech": part_of_speech,
        "notes": rest[0] if rest else "",
    }


def sync(model, existing: dict, desired: dict, key_of) -> dict:
    """Make the table match `desired` ({key: field values}) in bulk.

    `existing` maps keys to rows already in the database. Missing rows are
    created, rows whose values differ are updated, and the rest are left alone.
    Returns {key: row} for every desired key. Field values use attribute names
    (`chapter_id`), so foreign keys are compared by id without extra queries.
    """
    to_create, to_update, changed_fields = [], [], set()
    for key, values in desired.items():
        row = existing.get(key)
        if row is None:
            to_create.append(model(**values))
            continue
        diff = [f for f, v in values.items() if getattr(row, f) != v]
        if diff:
            for f in diff:
                setattr(row, f, values[f])
            to_update.append(row)
            changed_fields.update(diff)

    created = model.objects.bulk_create(to_create, batch_size=BATCH)
    if to_update:
        names = sorted(f.removesuffix("_id") if f.endswith("_id") else f for f in changed_fields)
        model.objects.bulk_update(to_update, names, batch_size=BATCH)

    rows = {key: existing[key] for key in desired if key in existing}
    rows.update({key_of(row): row for row in created})
    return rows


def delete_ids(model, ids) -> int:
    """Delete rows by id (with their cascades). Returns how many were asked for."""
    ids = list(ids)
    if ids:
        model.objects.filter(id__in=ids).delete()
    return len(ids)


class Command(BaseCommand):
    help = "Seed the learning path (every level, or --level). Safe to re-run."

    def add_arguments(self, parser):
        parser.add_argument(
            "--level", action="append", choices=list(LEVELS), help="Only this level (repeatable)."
        )

    def handle(self, *args, level=None, **options):
        for code in level or LEVELS:
            with transaction.atomic():
                if code == "A1":
                    legacy = Book.objects.filter(title__in=LEGACY_BOOKS)
                    titles = list(legacy.values_list("title", flat=True))
                    if titles:
                        self.stdout.write(f"Removing old books: {', '.join(titles)}")
                        legacy.delete()

                book, _ = Book.objects.get_or_create(
                    title=book_title(code), defaults={"description": f"The {code} learning path."}
                )
                counts = self._seed(book, code, LEVELS[code])

            self.stdout.write(self.style.SUCCESS(f"Seeded the {code} learning path:"))
            for k, v in counts.items():
                self.stdout.write(f"  {k}: {v}")

    def _seed(self, book, level: str, spec: dict) -> dict:
        removed = 0
        prefix = source_prefix(level)
        units_spec = {u["order"]: u for u in spec["units"]}

        # ---- chapters (one per unit) ----
        chapters = sync(
            Chapter,
            {c.number: c for c in Chapter.objects.filter(book=book)},
            {
                n: {
                    "book_id": book.id,
                    "number": n,
                    "title": u["title"],
                    "description": u["theme"],
                    "cefr_level": level,
                }
                for n, u in units_spec.items()
            },
            key_of=lambda c: c.number,
        )
        chapter_ids = [c.id for c in chapters.values()]

        # ---- words ----
        desired_words = {}
        for n, u in units_spec.items():
            for w in u["words"]:
                german, fields = word_fields(w)
                desired_words[(chapters[n].id, german)] = {
                    "chapter_id": chapters[n].id,
                    "german": german,
                    **fields,
                }
        existing_words = {
            (w.chapter_id, w.german): w for w in Word.objects.filter(chapter_id__in=chapter_ids)
        }
        words = sync(Word, existing_words, desired_words, lambda w: (w.chapter_id, w.german))
        removed += delete_ids(
            Word, (w.id for k, w in existing_words.items() if k not in desired_words)
        )

        # ---- grammar rules ----
        desired_rules = {
            (chapters[n].id, g["title"]): {
                "chapter_id": chapters[n].id,
                "title": g["title"],
                "category": g["category"],
                "content": g["content"],
                "example_sentences": g["examples"],
            }
            for n, u in units_spec.items()
            for g in u["grammar"]
        }
        existing_rules = {
            (r.chapter_id, r.title): r
            for r in GrammarRule.objects.filter(chapter_id__in=chapter_ids)
        }
        rules = sync(GrammarRule, existing_rules, desired_rules, lambda r: (r.chapter_id, r.title))
        removed += delete_ids(
            GrammarRule, (r.id for k, r in existing_rules.items() if k not in desired_rules)
        )

        # ---- units ----
        existing_units = {u.order: u for u in Unit.objects.filter(cefr_level=level)}
        units = sync(
            Unit,
            existing_units,
            {
                n: {
                    "cefr_level": level,
                    "order": n,
                    "title": u["title"],
                    "theme": u["theme"],
                    "accent_color": u["accent_color"],
                    "chapter_id": chapters[n].id,
                }
                for n, u in units_spec.items()
            },
            key_of=lambda u: u.order,
        )
        removed += delete_ids(
            Unit, (u.id for n, u in existing_units.items() if n not in units_spec)
        )
        removed += delete_ids(
            Chapter,
            Chapter.objects.filter(book=book, number__gt=len(spec["units"])).values_list(
                "id", flat=True
            ),
        )

        # ---- lessons ----
        # Keyed by title as well as position: a lesson whose title changes is a
        # different lesson, so it's replaced and its old progress goes with it.
        desired_lessons = {
            (units[n].id, les["order"], les["title"]): {
                "unit_id": units[n].id,
                "order": les["order"],
                "title": les["title"],
                "xp_reward": les.get("xp", 10),
            }
            for n, u in units_spec.items()
            for les in u["lessons"]
        }
        unit_ids = [u.id for u in units.values()]
        existing_lessons = {
            (les.unit_id, les.order, les.title): les
            for les in Lesson.objects.filter(unit_id__in=unit_ids)
        }
        # Delete first: a replaced lesson still holds its (unit, order) slot.
        removed += delete_ids(
            Lesson, (les.id for k, les in existing_lessons.items() if k not in desired_lessons)
        )
        lessons = sync(
            Lesson,
            {k: les for k, les in existing_lessons.items() if k in desired_lessons},
            desired_lessons,
            lambda les: (les.unit_id, les.order, les.title),
        )

        # ---- exercises (keyed by a stable source) ----
        desired_exercises, item_specs = {}, []
        for n, u in units_spec.items():
            for les in u["lessons"]:
                for idx, item in enumerate(les["items"]):
                    source = None
                    if item["kind"] == "exercise":
                        source = f"{prefix}u{n}-l{les['order']}-{idx}"
                        desired_exercises[source] = {
                            "source": source,
                            "chapter_id": chapters[n].id,
                            **exercise_fields(item),
                        }
                    item_specs.append((n, (les["order"], les["title"]), idx, item, source))
        # The checks' gap, translation and Modul-test exercises (no lesson items).
        for n, tasks in spec["lektion_checks"].items():
            for name, item in tasks.items():
                source = check_source(level, f"u{n}", name)
                desired_exercises[source] = {
                    "source": source,
                    "chapter_id": chapters[n].id,
                    **exercise_fields(item),
                }
        for m, tasks in spec["modul_checks"].items():
            for name, item in tasks.items():
                source = check_source(level, f"m{m}", name)
                desired_exercises[source] = {
                    "source": source,
                    "chapter_id": chapters[m * MODUL_SIZE].id,
                    **exercise_fields(item),
                }
        existing_exercises = {
            e.source: e for e in Exercise.objects.filter(source__startswith=prefix)
        }
        exercises = sync(Exercise, existing_exercises, desired_exercises, lambda e: e.source)

        # ---- lesson items ----
        desired_items = {}
        for n, (lorder, ltitle), idx, item, source in item_specs:
            lesson = lessons[(units[n].id, lorder, ltitle)]
            chapter_id = chapters[n].id
            desired_items[(lesson.id, idx)] = {
                "lesson_id": lesson.id,
                "order": idx,
                "kind": item["kind"],
                "exercise_id": exercises[source].id if source else None,
                "word_id": words[(chapter_id, item["word"])].id
                if item["kind"] == "review"
                else None,
                "grammar_rule_id": rules[(chapter_id, item["grammar"])].id
                if item["kind"] == "grammar"
                else None,
            }
        lesson_ids = [les.id for les in lessons.values()]
        existing_items = {
            (i.lesson_id, i.order): i for i in LessonItem.objects.filter(lesson_id__in=lesson_ids)
        }
        sync(LessonItem, existing_items, desired_items, lambda i: (i.lesson_id, i.order))
        removed += delete_ids(
            LessonItem, (i.id for k, i in existing_items.items() if k not in desired_items)
        )

        # ---- words each lesson teaches ----
        Taught = Lesson.words.through
        desired_taught = {}
        for n, u in units_spec.items():
            for les in u["lessons"]:
                lesson_id = lessons[(units[n].id, les["order"], les["title"])].id
                for german in les["teaches"]:
                    word_id = words[(chapters[n].id, german)].id
                    desired_taught[(lesson_id, word_id)] = {
                        "lesson_id": lesson_id,
                        "word_id": word_id,
                    }
        existing_taught = {
            (t.lesson_id, t.word_id): t for t in Taught.objects.filter(lesson_id__in=lesson_ids)
        }
        sync(Taught, existing_taught, desired_taught, lambda t: (t.lesson_id, t.word_id))
        delete_ids(Taught, (t.id for k, t in existing_taught.items() if k not in desired_taught))

        # Exercises from earlier runs that the content no longer has.
        removed += delete_ids(
            Exercise,
            (e.id for s, e in existing_exercises.items() if s not in desired_exercises),
        )

        return {
            "units": len(units),
            "lessons": len(lessons),
            "items": len(desired_items),
            "words": len(words),
            "grammar": len(rules),
            "exercises": len(exercises),
            "removed": removed,
        }
