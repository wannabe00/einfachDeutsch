"""Checks: reviewing and testing what a user has learned, like a teacher would.

Two kinds (see `Check`):

* **review** ("Wiederholung") of one finished Lektion: about a third of its
  words (30 words -> 10, 60 -> 20; at least 5, in steps of 5), weak words
  first and the rest at random, shown in batches of five; then the Lektion's
  gap task and translation task.
* **modul** test after every three Lektionen: words from the Modul and from
  earlier Lektionen, the gap and translation tasks of the Modul's Lektionen and
  of a couple of earlier ones, and the Modul's extra formats (dialogue,
  question and answer, reading, odd one out, forming words, finding mistakes,
  dictation). The result is scored per skill.

The difficulty ramp (`content.dsl.STAGES`) decides the formats: early
Lektionen only ask to recognise (pick, match, chips), later ones to type.

Word tasks are generated from the word list, so their ids say everything
needed to rebuild and grade them: "w:12.pick_de,15.article" (a batch, each word
with its format) and "m:12,15,18" (a matching batch). Distractors are chosen
deterministically from the word's chapter. Authored tasks are seeded exercises,
"e:<exercise id>". Answers to word tasks move the words through SM-2 like a
flashcard. Grading is local, so free users get checks too; they never cost
energy.
"""

import random
from collections import defaultdict
from datetime import date, timedelta

from django.utils import timezone

from apps.accounts.levels import level_rank, visible_levels
from apps.accounts.scheduling import record_activity
from apps.exercises.models import Exercise, ExerciseAttempt
from apps.vocabulary.models import Word, WordProgress
from apps.vocabulary.progress import record_review

from . import grading
from .content.dsl import ARTICLES, STAGES, stage_of
from .learned import finished_units, learned_word_ids
from .models import Check, Unit

MODUL_SIZE = 3  # Lektionen per Modul
BATCH = 5
REVIEW_SHARE = 3  # a review asks about a third of a Lektion's words
MAX_REVIEW_WORDS = 30
MODUL_WORDS = 10  # from the Modul's own Lektionen
EARLIER_WORDS = 5  # from the Lektionen before it
EARLIER_TASKS = 2  # gap or translation tasks from earlier Lektionen
EARLIER_EXTRAS = 2  # extra-format tasks from earlier Moduls
RESUME_DAYS = 7  # an unfinished check older than this starts over
RIGHT, WRONG = 4, 0  # SM-2 quality for a word answered right / wrong

SKILLS = ("words", "grammar", "listening", "reading")
# The skill an authored task tests, by its name in the content.
TASK_SKILL = {
    "gap": "words",
    "odd": "words",
    "translate": "grammar",
    "form": "grammar",
    "mistake": "grammar",
    "dictation": "listening",
    "dialogue": "reading",
    "qa": "reading",
    "reading": "reading",
}
EXTRA_ORDER = ("dialogue", "qa", "reading", "odd", "form", "mistake", "dictation")


class CheckError(Exception):
    """A check or task that isn't the user's (or doesn't exist yet)."""


def _source_base(level: str) -> str:
    return f"seed-{level.lower()}-check-"


def check_source(level: str, where: str, name: str) -> str:
    """The `Exercise.source` of an authored check task, e.g. 'seed-a1-check-u3-gap'
    (Lektion 3's gap task) or 'seed-a1-check-m2-reading' (Modul 2's reading)."""
    return f"{_source_base(level)}{where}-{name}"


def review_size(word_count: int) -> int:
    """How many words a review asks: a third, in steps of five, at least five."""
    if word_count <= BATCH:
        return word_count
    size = round(word_count / REVIEW_SHARE / BATCH) * BATCH
    return max(BATCH, min(MAX_REVIEW_WORDS, size))


# ---- picking words ---------------------------------------------------------


def _pick_words(user, words: list[Word], k: int) -> list[Word]:
    """Weak words first (got wrong before, low ease, or due), weakest first;
    then the others at random."""
    progress = {p.word_id: p for p in WordProgress.objects.filter(user=user, word__in=words)}
    today = date.today()

    def weakness(word):
        p = progress.get(word.id)
        if p is None or not (p.times_wrong or p.ease_factor < 2.5 or p.next_review <= today):
            return None
        return (p.ease_factor, -p.times_wrong, random.random())

    weak = sorted((w for w in words if weakness(w)), key=weakness)
    rest = [w for w in words if not weakness(w)]
    random.shuffle(rest)
    return (weak + rest)[:k]


def _has_article(word: Word) -> bool:
    head, _, rest = word.german.partition(" ")
    return word.part_of_speech == "noun" and head in ARTICLES and bool(rest)


def _word_tasks(words: list[Word], stage: int) -> list[dict]:
    """Batches of five: a matching batch every other time where the stage
    allows it, else one part per word in a format the stage allows."""
    rules = STAGES[stage]
    tasks = []
    for i in range(0, len(words), BATCH):
        batch = words[i : i + BATCH]
        if rules["match_batches"] and (i // BATCH) % 2 == 1 and len(batch) >= 3:
            tasks.append({"id": "m:" + ",".join(str(w.id) for w in batch), "skill": "words"})
            continue
        specs = []
        for word in batch:
            formats = [f for f in rules["words"] if f != "article" or _has_article(word)]
            specs.append(f"{word.id}.{random.choice(formats)}")
        tasks.append({"id": "w:" + ",".join(specs), "skill": "words"})
    return tasks


# ---- building word parts (the same every time for the same task id) --------


def _stable_shuffle(items: list, key: str) -> list:
    items = list(items)
    random.Random(key).shuffle(items)
    return items


def _distractors(word: Word, pool: list[Word], field: str, k: int, key: str) -> list[str]:
    """`k` other values of `field` from the chapter, same part of speech first."""
    seen = {getattr(word, field).casefold()}
    same, other = [], []
    for w in sorted(pool, key=lambda w: w.id):
        value = getattr(w, field)
        if value.casefold() in seen:
            continue
        seen.add(value.casefold())
        (same if w.part_of_speech == word.part_of_speech else other).append(value)
    rng = random.Random(key)
    rng.shuffle(same)
    rng.shuffle(other)
    return (same + other)[:k]


def _word_part(word: Word, fmt: str, pool: list[Word]) -> dict:
    key = f"{word.id}-{fmt}"
    if fmt == "article":
        article, bare = word.german.split(" ", 1)
        return {
            "type": "multiple_choice",
            "prompt": f"___ {bare}",
            "hint": word.english,
            "options": list(ARTICLES),
            "answer": article,
        }
    if fmt == "type_de":
        return {
            "type": "translation",
            "prompt": f"In German: “{word.english}”",
            "hint": "with the article" if _has_article(word) else "",
            "answer": word.german,
        }
    if fmt == "pick_en":
        wrong = _distractors(word, pool, "english", 3, key)
        return {
            "type": "multiple_choice",
            "prompt": f"What does „{word.german}“ mean?",
            "hint": "",
            "options": _stable_shuffle([word.english, *wrong], key),
            "answer": word.english,
        }
    wrong = _distractors(word, pool, "german", 3, key)
    part = {
        "type": "multiple_choice",
        "prompt": f"German for “{word.english}”?",
        "hint": "",
        "options": _stable_shuffle([word.german, *wrong], key),
        "answer": word.german,
    }
    if fmt == "listen":
        part.update(prompt="Which word do you hear?", say=word.german)
    return part


class _Loaded:
    """Everything a check's tasks need, loaded in a few queries."""

    def __init__(self, task_ids: list[str]):
        word_ids, exercise_ids = set(), set()
        for task_id in task_ids:
            kind, _, rest = task_id.partition(":")
            if kind == "e":
                exercise_ids.add(int(rest))
            else:
                word_ids |= {int(spec.split(".")[0]) for spec in rest.split(",")}
        self.words = {w.id: w for w in Word.objects.filter(id__in=word_ids)}
        chapters = {w.chapter_id for w in self.words.values()}
        self.pool: dict[int, list[Word]] = defaultdict(list)
        for w in Word.objects.filter(chapter_id__in=chapters):
            self.pool[w.chapter_id].append(w)
        self.exercises = {e.id: e for e in Exercise.objects.filter(id__in=exercise_ids)}

    def task(self, task_id: str):
        """(parts, exercise or None, [(word, fmt) per part] or a matching batch's words)."""
        kind, _, rest = task_id.partition(":")
        try:
            if kind == "e":
                exercise = self.exercises[int(rest)]
                return grading.parts_of(exercise), exercise, []
            if kind == "m":
                words = [self.words[int(i)] for i in rest.split(",")]
                part = {
                    "type": "matching",
                    "prompt": "Match the German to the English.",
                    "hint": "",
                    "pairs": [[w.german, w.english] for w in words],
                }
                return [part], None, [(w, "match") for w in words]
            if kind == "w":
                specs = [spec.split(".") for spec in rest.split(",")]
                pairs = [(self.words[int(i)], fmt) for i, fmt in specs]
                parts = [_word_part(w, fmt, self.pool[w.chapter_id]) for w, fmt in pairs]
                return parts, None, pairs
        except (KeyError, ValueError) as err:
            raise CheckError("Unknown task.") from err
        raise CheckError("Unknown task.")

    def public(self, task: dict) -> dict:
        """A task as the client sees it: no answers."""
        parts, exercise, words = self.task(task["id"])
        if exercise is not None:
            out = grading.public_exercise(exercise)
            out.pop("exercise_id")
        elif len(parts) == 1:
            out = grading.public_part(parts[0])
        else:
            lektionen = {self.words[w.id].chapter_id for w, _ in words}
            prompt = "Words you've learned"
            if len(lektionen) == 1:
                prompt = f"Words from Lektion {words[0][0].chapter.number}"
            out = {
                "type": "group",
                "prompt": prompt,
                "hint": "",
                "payload": {"parts": [grading.public_part(p) for p in parts]},
            }
        return {**out, "task_id": task["id"], "skill": task["skill"]}


def _part_skills(task: dict) -> list[str]:
    """The skill each part of a task counts towards."""
    kind, _, rest = task["id"].partition(":")
    if kind == "w":
        return ["listening" if spec.endswith(".listen") else "words" for spec in rest.split(",")]
    return [task["skill"]]


# ---- what can be checked ----------------------------------------------------


def _reviewable_units(user) -> list[Unit]:
    """Finished units, plus every unit of the levels below the user's (they
    were placed or promoted past them)."""
    level = user.profile.cefr_level
    finished = finished_units(user)
    units = Unit.objects.filter(cefr_level__in=visible_levels(level)).select_related("chapter")
    return [
        u
        for u in sorted(units, key=lambda u: (level_rank(u.cefr_level), u.order))
        if u.id in finished or level_rank(u.cefr_level) < level_rank(level)
    ]


def _unit_summary(unit: Unit) -> dict:
    return {
        "id": unit.id,
        "order": unit.order,
        "title": unit.title,
        "cefr_level": unit.cefr_level,
    }


def _open_check(user, **filters) -> Check | None:
    since = timezone.now() - timedelta(days=RESUME_DAYS)
    return Check.objects.filter(
        user=user, completed_at__isnull=True, started_at__gte=since, **filters
    ).first()


def status(user) -> dict:
    """What the user can check: the last finished Lektion (for the Dashboard),
    every reviewable Lektion, and the Modul tests with their best scores."""
    reviewable = _reviewable_units(user)
    finished = finished_units(user)
    last_id = max(finished, key=finished.get) if finished else None
    done_ids = {u.id for u in reviewable}

    by_level: dict[str, dict[int, Unit]] = defaultdict(dict)
    for unit in Unit.objects.filter(cefr_level__in=visible_levels(user.profile.cefr_level)):
        by_level[unit.cefr_level][unit.order] = unit

    best: dict[tuple, float] = {}
    for c in Check.objects.filter(user=user, kind=Check.Kind.MODUL, completed_at__isnull=False):
        key = (c.cefr_level, c.modul)
        best[key] = max(best.get(key, 0), c.score or 0)
    open_moduls = {
        (c.cefr_level, c.modul)
        for c in Check.objects.filter(
            user=user,
            kind=Check.Kind.MODUL,
            completed_at__isnull=True,
            started_at__gte=timezone.now() - timedelta(days=RESUME_DAYS),
        )
    }

    moduls = []
    for level in sorted(by_level, key=level_rank):
        units = by_level[level]
        for modul in range(1, max(units, default=0) // MODUL_SIZE + 1):
            last = modul * MODUL_SIZE
            if any(n not in units for n in range(last - MODUL_SIZE + 1, last + 1)):
                continue
            moduls.append(
                {
                    "cefr_level": level,
                    "modul": modul,
                    "first": last - MODUL_SIZE + 1,
                    "last": last,
                    "unlocked": all(
                        units[n].id in done_ids for n in range(1, last + 1) if n in units
                    ),
                    "best_score": best.get((level, modul)),
                    "in_progress": (level, modul) in open_moduls,
                }
            )

    last_unit = next((u for u in reviewable if u.id == last_id), None)
    return {
        "last_unit": _unit_summary(last_unit) if last_unit else None,
        "units": [_unit_summary(u) for u in reviewable],
        "moduls": moduls,
    }


# ---- starting a check -------------------------------------------------------


def _authored(level: str, names: list[str]) -> list[dict]:
    """Tasks for authored exercises named like 'u3-gap' or 'm2-reading', in the
    order given; names without content are skipped."""
    sources = {check_source(level, *name.split("-", 1)): name for name in names}
    found = {e.source: e.id for e in Exercise.objects.filter(source__in=sources)}
    return [
        {"id": f"e:{found[src]}", "skill": TASK_SKILL[name.split("-", 1)[1]]}
        for src, name in sources.items()
        if src in found
    ]


def _learned_words(user, units: list[Unit]) -> list[Word]:
    learned = learned_word_ids(user)
    chapters = [u.chapter_id for u in units if u.chapter_id]
    return list(Word.objects.filter(chapter_id__in=chapters, id__in=learned))


def _review_tasks(user, unit: Unit) -> list[dict]:
    words = _learned_words(user, [unit])
    picked = _pick_words(user, words, review_size(len(words)))
    stage = stage_of(unit.cefr_level, unit.order)
    tasks = _word_tasks(picked, stage)
    return tasks + _authored(unit.cefr_level, [f"u{unit.order}-gap", f"u{unit.order}-translate"])


def _modul_tasks(user, level: str, modul: int, units: dict[int, Unit]) -> list[dict]:
    last = modul * MODUL_SIZE
    first = last - MODUL_SIZE + 1
    own = [units[n] for n in range(first, last + 1)]
    earlier = [u for n, u in units.items() if n < first]

    own_words = _learned_words(user, own)
    earlier_words = _learned_words(user, earlier)
    from_earlier = EARLIER_WORDS if earlier_words else 0
    words = _pick_words(user, own_words, MODUL_WORDS + EARLIER_WORDS - from_earlier)
    words += _pick_words(user, earlier_words, from_earlier)
    random.shuffle(words)
    tasks = _word_tasks(words, stage_of(level, last))

    names = [f"u{n}-{kind}" for n in range(first, last + 1) for kind in ("gap", "translate")]
    earlier_names = [f"u{u.order}-{kind}" for u in earlier for kind in ("gap", "translate")]
    names += random.sample(earlier_names, min(EARLIER_TASKS, len(earlier_names)))

    extras = [f"m{modul}-{kind}" for kind in EXTRA_ORDER]
    base = _source_base(level)
    earlier_extras = []
    for source in Exercise.objects.filter(source__startswith=f"{base}m").values_list(
        "source", flat=True
    ):
        name = source.removeprefix(base)  # 'm2-reading'
        number = name.split("-", 1)[0][1:]
        if number.isdigit() and int(number) < modul:
            earlier_extras.append(name)
    extras += random.sample(earlier_extras, min(EARLIER_EXTRAS, len(earlier_extras)))
    return tasks + _authored(level, names) + _authored(level, extras)


def start(user, kind: str, unit_id=None, level=None, modul=None) -> Check:
    """Resume the user's unfinished check of the same thing, or start a new one."""
    reviewable = {u.id: u for u in _reviewable_units(user)}
    if kind == Check.Kind.REVIEW:
        unit = reviewable.get(unit_id)
        if unit is None:
            raise CheckError("You can review a Lektion once you've finished it.")
        existing = _open_check(user, kind=kind, unit=unit)
        if existing:
            return existing
        tasks = _review_tasks(user, unit)
        fields = {"unit": unit, "cefr_level": unit.cefr_level}
    elif kind == Check.Kind.MODUL:
        units = {u.order: u for u in reviewable.values() if u.cefr_level == level}
        last = (modul or 0) * MODUL_SIZE
        if not modul or any(n not in units for n in range(1, last + 1)):
            raise CheckError("Finish the Modul's Lektionen to unlock its test.")
        existing = _open_check(user, kind=kind, cefr_level=level, modul=modul)
        if existing:
            return existing
        scope = {n: u for n, u in units.items() if n <= last}
        tasks = _modul_tasks(user, level, modul, scope)
        fields = {"unit": units[last], "cefr_level": level, "modul": modul}
    else:
        raise CheckError("Unknown kind of check.")

    if not tasks:
        raise CheckError("There's nothing to check here yet.")
    return Check.objects.create(user=user, kind=kind, tasks=tasks, **fields)


# ---- answering and finishing ------------------------------------------------


def get_check(user, check_id: int) -> Check:
    check = Check.objects.filter(id=check_id, user=user).select_related("unit").first()
    if check is None:
        raise CheckError("Unknown check.")
    return check


def answer(user, check: Check, task_id: str, given) -> dict:
    """Grade one task of `check`, record it, and reveal the solution. Answering
    the same task again returns the first result."""
    if check.completed_at:
        raise CheckError("This check is finished.")
    task = next((t for t in check.tasks if t["id"] == task_id), None)
    if task is None:
        raise CheckError("That task isn't part of this check.")
    if task_id in check.results:
        return check.results[task_id]

    parts, exercise, words = _Loaded([task_id]).task(task_id)
    if exercise is not None:
        verdicts = grading.grade_parts(exercise, given)
        solution = grading.solution_of(exercise)
        ExerciseAttempt.objects.create(
            user=user, exercise=exercise, user_answer=str(given), is_correct=all(verdicts)
        )
    else:
        answers = [given] if len(parts) == 1 else (given if isinstance(given, list) else [])
        verdicts = [
            grading.grade_part(p, answers[i] if i < len(answers) else None)
            for i, p in enumerate(parts)
        ]
        solutions = [grading.solution_of_part(p) for p in parts]
        solution = solutions[0] if len(parts) == 1 else solutions
        _review_words(user, parts, words, answers, verdicts)

    result = {
        "correct": bool(verdicts) and all(verdicts),
        "parts": verdicts,
        "solution": solution,
        "explanation": exercise.explanation if exercise else "",
    }
    check.results = {**check.results, task_id: result}
    check.save(update_fields=["results"])
    record_activity(user)
    return result


def _review_words(user, parts, words, answers, verdicts) -> None:
    """Move each word of a word task through SM-2. In a matching batch every
    pair counts on its own."""
    if parts and parts[0]["type"] == "matching":
        given = answers[0] if answers and isinstance(answers[0], dict) else {}
        for word, _ in words:
            ok = grading.normalize(given.get(word.german, "")) == grading.normalize(word.english)
            record_review(user, word, RIGHT if ok else WRONG)
        return
    for (word, _), ok in zip(words, verdicts, strict=True):
        record_review(user, word, RIGHT if ok else WRONG)


def finish(user, check: Check) -> Check:
    """Score a check once every task is answered: overall and per skill."""
    if check.completed_at:
        return check
    missing = [t["id"] for t in check.tasks if t["id"] not in check.results]
    if missing:
        raise CheckError("Answer every task first.")
    skills = {s: [0, 0] for s in SKILLS}
    for task in check.tasks:
        verdicts = check.results[task["id"]]["parts"]
        part_skills = _part_skills(task)
        for i, ok in enumerate(verdicts):
            skill = part_skills[i] if i < len(part_skills) else task["skill"]
            skills[skill][0] += int(bool(ok))
            skills[skill][1] += 1
    right = sum(r for r, _ in skills.values())
    total = sum(t for _, t in skills.values())
    check.skills = {s: v for s, v in skills.items() if v[1]}
    check.score = right / total if total else 0
    check.completed_at = timezone.now()
    check.save(update_fields=["skills", "score", "completed_at"])
    return check


def payload(check: Check) -> dict:
    """A check as the client sees it, with the results so far."""
    loaded = _Loaded([t["id"] for t in check.tasks])
    unit = check.unit
    if check.kind == Check.Kind.MODUL:
        first = check.modul * MODUL_SIZE - MODUL_SIZE + 1
        title = f"Modul {check.modul} test"
        subtitle = f"{check.cefr_level} · Lektionen 1-{unit.order}, focus on {first}-{unit.order}"
    else:
        title = f"Wiederholung: Lektion {unit.order}"
        subtitle = unit.title
    return {
        "id": check.id,
        "kind": check.kind,
        "cefr_level": check.cefr_level,
        "modul": check.modul,
        "unit": _unit_summary(unit),
        "title": title,
        "subtitle": subtitle,
        "tasks": [loaded.public(t) for t in check.tasks],
        "results": check.results,
        "completed": check.completed_at is not None,
        "score": check.score,
        "skills": {s: {"right": r, "total": t} for s, (r, t) in check.skills.items()},
    }
