"""CEFR placement test + level progression engine (Phase 14).

The placement test is an authored multiple-choice set (original content, not from
any copyrighted book), graded locally — reliable and free, no AI quota needed.
Each question is tagged with the level it demonstrates; a user "passes" a level
by getting most of its questions right, and we suggest the highest level they
pass consecutively from A1 upward (capped at B2; C1/C2 are chosen manually).
"""

from __future__ import annotations

# Ordered levels the placement test can assign.
PLACEMENT_LEVELS = ["A1", "A2", "B1", "B2"]

# id, level, prompt, options, answer (must be one of options)
PLACEMENT_QUESTIONS = [
    {
        "id": "a1_1",
        "level": "A1",
        "prompt": "___ heißt du? — Ich heiße Anna.",
        "options": ["Wie", "Wo", "Was", "Wer"],
        "answer": "Wie",
    },
    {
        "id": "a1_2",
        "level": "A1",
        "prompt": "Das ist ein Hund. ___ Hund ist groß.",
        "options": ["Der", "Die", "Das", "Den"],
        "answer": "Der",
    },
    {
        "id": "a1_3",
        "level": "A1",
        "prompt": "Ich ___ aus Italien.",
        "options": ["komme", "kommst", "kommen", "kommt"],
        "answer": "komme",
    },
    {
        "id": "a2_1",
        "level": "A2",
        "prompt": "Gestern ___ ich ins Kino gegangen.",
        "options": ["bin", "habe", "war", "ist"],
        "answer": "bin",
    },
    {
        "id": "a2_2",
        "level": "A2",
        "prompt": "Ich gebe ___ Freund ein Buch.",
        "options": ["meinem", "mein", "meinen", "meines"],
        "answer": "meinem",
    },
    {
        "id": "a2_3",
        "level": "A2",
        "prompt": "Wir treffen uns ___ Montag.",
        "options": ["am", "im", "um", "an"],
        "answer": "am",
    },
    {
        "id": "b1_1",
        "level": "B1",
        "prompt": "Ich weiß nicht, ob er heute ___.",
        "options": ["kommt", "kommen", "gekommen", "zu kommen"],
        "answer": "kommt",
    },
    {
        "id": "b1_2",
        "level": "B1",
        "prompt": "Das ist der Mann, ___ Auto gestohlen wurde.",
        "options": ["dessen", "den", "der", "dem"],
        "answer": "dessen",
    },
    {
        "id": "b1_3",
        "level": "B1",
        "prompt": "Wenn ich Zeit hätte, ___ ich dir helfen.",
        "options": ["würde", "werde", "wurde", "habe"],
        "answer": "würde",
    },
    {
        "id": "b2_1",
        "level": "B2",
        "prompt": "Der Vertrag muss bis morgen ___ werden.",
        "options": ["unterschrieben", "unterschreiben", "unterschreibt", "unterschrieb"],
        "answer": "unterschrieben",
    },
    {
        "id": "b2_2",
        "level": "B2",
        "prompt": "___ des schlechten Wetters fand das Spiel statt.",
        "options": ["Trotz", "Wegen", "Während", "Statt"],
        "answer": "Trotz",
    },
    {
        "id": "b2_3",
        "level": "B2",
        "prompt": "Je mehr man übt, ___ besser wird man.",
        "options": ["desto", "umso mehr", "als", "wie"],
        "answer": "desto",
    },
]

PASS_RATIO = 0.6  # share of a level's questions needed to "pass" it


def public_questions() -> list[dict]:
    """Questions without the answers (safe to send to the client)."""
    return [
        {"id": q["id"], "level": q["level"], "prompt": q["prompt"], "options": q["options"]}
        for q in PLACEMENT_QUESTIONS
    ]


def grade_placement(answers: dict) -> dict:
    """`answers` maps question id -> chosen option. Returns the suggested level
    plus the per-level breakdown."""
    by_level: dict[str, list[bool]] = {lvl: [] for lvl in PLACEMENT_LEVELS}
    correct_total = 0
    for q in PLACEMENT_QUESTIONS:
        chosen = str(answers.get(q["id"], "")).strip()
        ok = chosen == q["answer"]
        by_level[q["level"]].append(ok)
        correct_total += 1 if ok else 0

    suggested = "A1"
    for lvl in PLACEMENT_LEVELS:
        results = by_level[lvl]
        ratio = (sum(results) / len(results)) if results else 0
        if ratio >= PASS_RATIO:
            suggested = lvl
        else:
            break  # stop at the first level they don't pass

    return {
        "suggested_level": suggested,
        "correct": correct_total,
        "total": len(PLACEMENT_QUESTIONS),
        "per_level": {
            lvl: {"correct": sum(by_level[lvl]), "total": len(by_level[lvl])}
            for lvl in PLACEMENT_LEVELS
        },
    }


def evaluate_level(user) -> dict:
    """Progression status for `user`: current level, requirements, and whether
    they've completed enough to advance (completion-gated, not XP)."""
    from apps.vocabulary.models import ReviewLog

    from .models import LevelDefinition, UserLessonProgress

    profile = user.profile
    current = profile.cefr_level
    completed_lessons = UserLessonProgress.objects.filter(user=user).count()
    total_reviews = ReviewLog.objects.filter(user=user).count()

    current_def = LevelDefinition.objects.filter(cefr_level=current).first()
    next_def = None
    can_advance = False
    if current_def:
        req_lessons = current_def.required_lessons
        req_reviews = current_def.required_reviews
        can_advance = completed_lessons >= req_lessons and total_reviews >= req_reviews
        next_def = (
            LevelDefinition.objects.filter(order__gt=current_def.order).order_by("order").first()
        )
    else:
        req_lessons = req_reviews = 0

    return {
        "current_level": current,
        "next_level": next_def.cefr_level if next_def else None,
        "required_lessons": req_lessons,
        "required_reviews": req_reviews,
        "completed_lessons": completed_lessons,
        "total_reviews": total_reviews,
        "can_advance": can_advance,
    }
