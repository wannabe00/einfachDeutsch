"""Checks on the path content files, run before anything is seeded.

Every exercise is built the way the seed command builds it and graded with the
real grader: its own answer must pass and an obviously wrong one must fail.
"""

from collections import Counter

from django.test import SimpleTestCase

from apps.curriculum.content.a1 import A1_UNITS
from apps.curriculum.content.dsl import DEFAULT_MAX_PARTS, art, fill, group
from apps.curriculum.grading import grade_parts, public_exercise, solution_of
from apps.curriculum.management.commands.seed_a1_path import exercise_fields
from apps.exercises.models import Exercise
from apps.grammar.models import GrammarRule
from apps.vocabulary.pos import PART_OF_SPEECH_CHOICES

POS = {value for value, _ in PART_OF_SPEECH_CHOICES}
CATEGORIES = {value for value, _ in GrammarRule.CATEGORY_CHOICES}
# A unit is 2-3 lessons of about 20-30 minutes; a screen is one item.
LESSONS_PER_UNIT = (2, 3)
MAX_SCREENS_PER_LESSON = 40


def right_answer(item):
    t = item["type"]
    if t == "group":
        return [right_answer(p) for p in item["parts"]]
    if t in ("multiple_choice", "sentence_order"):
        return item["answer"]
    if t == "word_bank":
        return item["answers"]
    if t == "matching":
        return {left: right for left, right in item["pairs"]}
    return item["answer"].split("|")[0]


def wrong_answer(item):
    t = item["type"]
    if t == "group":
        return [wrong_answer(p) for p in item["parts"]]
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
    """Every exercise, with a multi-part one's parts listed after it."""
    for les in unit["lessons"]:
        for item in les["items"]:
            if item["kind"] == "exercise":
                yield les, item
                for part in item.get("parts", []):
                    yield les, part


def single_exercises(unit):
    """Every exercise and part that holds an answer of its own."""
    return ((les, i) for les, i in exercises(unit) if i["type"] != "group")


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
            self.assertIn(len(u["lessons"]), LESSONS_PER_UNIT, u["title"])
            for les in u["lessons"]:
                where = f"unit {u['order']} / {les['title']}"
                self.assertTrue(les["items"], where)
                self.assertLessEqual(len(les["items"]), MAX_SCREENS_PER_LESSON, where)
                for item in les["items"]:
                    if item["kind"] == "review":
                        self.assertIn(item["word"], words, where)
                    elif item["kind"] == "grammar":
                        self.assertIn(item["grammar"], rules, where)

    def test_every_word_is_taught_by_exactly_one_lesson(self):
        for u in A1_UNITS:
            taught = [g for les in u["lessons"] for g in les["teaches"]]
            self.assertCountEqual(taught, [w[1] for w in u["words"]], u["title"])

    def test_every_exercise_grades_correctly(self):
        for u in A1_UNITS:
            for les, item in exercises(u):
                where = f"unit {u['order']} / {les['title']} / {item['prompt']!r}"
                ex = Exercise(**exercise_fields(item))
                self.assertTrue(
                    all(grade_parts(ex, right_answer(item))), f"Own answer fails: {where}"
                )
                self.assertFalse(
                    all(grade_parts(ex, wrong_answer(item))), f"Wrong answer passes: {where}"
                )
                if item["type"] == "group":
                    self.assertGreaterEqual(len(item["parts"]), 2, where)
                    self.assertLessEqual(len(item["parts"]), DEFAULT_MAX_PARTS, where)
                    self.assertFalse(any(grade_parts(ex, wrong_answer(item))), where)
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
                for _, i in single_exercises(u)
            ]
            dupes = [k for k, n in Counter(keys).items() if n > 1]
            self.assertFalse(dupes, f"Unit {u['order']} repeats: {dupes[:3]}")

    def test_no_em_dashes(self):
        for u in A1_UNITS:
            for _, item in exercises(u):
                self.assertNotIn("—", str(item), item["prompt"])


class GroupGradingTests(SimpleTestCase):
    def setUp(self):
        item = group(
            "Choose the article.", art("der Tisch"), art("die Lampe"), fill("Ich ___.", "bin")
        )
        self.ex = Exercise(**exercise_fields(item))

    def test_each_part_is_marked(self):
        self.assertEqual(grade_parts(self.ex, ["der", "das", "bin"]), [True, False, True])
        self.assertFalse(all(grade_parts(self.ex, ["der", "das", "bin"])))
        self.assertTrue(all(grade_parts(self.ex, ["der", "die", "bin"])))

    def test_missing_or_malformed_answers_score_nothing(self):
        self.assertEqual(grade_parts(self.ex, ["der"]), [True, False, False])
        self.assertEqual(grade_parts(self.ex, "der"), [False, False, False])

    def test_the_client_never_sees_answers(self):
        public = public_exercise(self.ex)
        self.assertEqual(public["type"], "group")
        self.assertEqual(len(public["payload"]["parts"]), 3)
        self.assertNotIn("answer", str(public))
        self.assertEqual(solution_of(self.ex), [["der"], ["die"], ["bin"]])
