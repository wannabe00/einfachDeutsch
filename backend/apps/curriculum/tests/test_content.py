"""Checks on the path content files, run before anything is seeded.

Every exercise is built the way the seed command builds it and graded with the
real grader: its own answer must pass and an obviously wrong one must fail.
"""

from collections import Counter

from django.test import SimpleTestCase

from apps.curriculum.content.a1 import A1_UNITS
from apps.curriculum.grading import grade
from apps.curriculum.management.commands.seed_a1_path import exercise_fields
from apps.exercises.models import Exercise
from apps.grammar.models import GrammarRule
from apps.vocabulary.pos import PART_OF_SPEECH_CHOICES

POS = {value for value, _ in PART_OF_SPEECH_CHOICES}
CATEGORIES = {value for value, _ in GrammarRule.CATEGORY_CHOICES}
MAX_ITEMS_PER_LESSON = 12


def right_answer(item):
    t = item["type"]
    if t in ("multiple_choice", "sentence_order"):
        return item["answer"]
    if t == "word_bank":
        return item["answers"]
    if t == "matching":
        return {left: right for left, right in item["pairs"]}
    return item["answer"].split("|")[0]


def wrong_answer(item):
    t = item["type"]
    if t == "multiple_choice":
        return next(o for o in item["options"] if o != item["answer"])
    if t == "sentence_order":
        return list(reversed(item["answer"]))
    if t == "word_bank":
        return ["xxx"] * len(item["answers"])
    if t == "matching":
        return {}
    return "xxx"


def exercises(unit):
    for les in unit["lessons"]:
        for item in les["items"]:
            if item["kind"] == "exercise":
                yield les, item


class ContentTests(SimpleTestCase):
    def test_units_are_numbered_in_order(self):
        self.assertEqual([u["order"] for u in A1_UNITS], list(range(1, len(A1_UNITS) + 1)))

    def test_words(self):
        seen = {}
        for u in A1_UNITS:
            germans = [w[1] for w in u["words"]]
            dupes = [g for g, n in Counter(germans).items() if n > 1]
            self.assertFalse(dupes, f"Unit {u['order']} lists twice: {dupes}")
            for w in u["words"]:
                self.assertIn(len(w), (3, 4), w)
                self.assertIn(w[2], POS, w)
                key = w[1].lower()
                if key in seen:
                    self.fail(f"{w[1]!r} is in unit {seen[key]} and unit {u['order']}")
                seen[key] = u["order"]

    def test_english_meanings_are_unique_within_a_unit(self):
        # Generated "what does X mean?" and translation drills rely on this.
        for u in A1_UNITS:
            english = [w[0] for w in u["words"]]
            dupes = [e for e, n in Counter(english).items() if n > 1]
            self.assertFalse(dupes, f"Unit {u['order']} has two words meaning {dupes}")

    def test_grammar_rules_are_valid_and_taught(self):
        for u in A1_UNITS:
            titles = [g["title"] for g in u["grammar"]]
            self.assertEqual(len(titles), len(set(titles)), u["title"])
            taught = {
                i["grammar"] for les in u["lessons"] for i in les["items"] if i["kind"] == "grammar"
            }
            for g in u["grammar"]:
                self.assertIn(g["category"], CATEGORIES, g["title"])
                self.assertIn(g["title"], taught, f"No lesson teaches {g['title']!r}")

    def test_lessons_and_references(self):
        for u in A1_UNITS:
            words = {w[1] for w in u["words"]}
            rules = {g["title"] for g in u["grammar"]}
            self.assertTrue(u["lessons"], u["title"])
            for les in u["lessons"]:
                where = f"unit {u['order']} / {les['title']}"
                self.assertTrue(les["items"], where)
                self.assertLessEqual(len(les["items"]), MAX_ITEMS_PER_LESSON, where)
                for item in les["items"]:
                    if item["kind"] == "review":
                        self.assertIn(item["word"], words, where)
                    elif item["kind"] == "grammar":
                        self.assertIn(item["grammar"], rules, where)

    def test_every_exercise_grades_correctly(self):
        for u in A1_UNITS:
            for les, item in exercises(u):
                where = f"unit {u['order']} / {les['title']} / {item['prompt']!r}"
                ex = Exercise(**exercise_fields(item))
                self.assertTrue(grade(ex, right_answer(item)), f"Own answer fails: {where}")
                self.assertFalse(grade(ex, wrong_answer(item)), f"Wrong answer passes: {where}")
                if item["type"] == "multiple_choice":
                    self.assertEqual(len(item["options"]), len(set(item["options"])), where)
                    self.assertGreaterEqual(len(item["options"]), 2, where)
                if item["type"] in ("translation", "fill_blank", "article", "conjugation"):
                    self.assertNotIn("…", item["answer"], f"Answer can't be typed: {where}")
                if item["type"] == "sentence_order":
                    self.assertEqual(sorted(item["tokens"]), sorted(item["answer"]), where)
                    self.assertGreaterEqual(len(item["answer"]), 3, where)

    def test_no_repeated_exercises_within_a_unit(self):
        for u in A1_UNITS:
            keys = [
                (i["type"], i["prompt"], str(right_answer(i)), i.get("text", ""))
                for _, i in exercises(u)
            ]
            dupes = [k for k, n in Counter(keys).items() if n > 1]
            self.assertFalse(dupes, f"Unit {u['order']} repeats: {dupes[:3]}")

    def test_no_em_dashes(self):
        for u in A1_UNITS:
            for _, item in exercises(u):
                self.assertNotIn("—", str(item), item["prompt"])
