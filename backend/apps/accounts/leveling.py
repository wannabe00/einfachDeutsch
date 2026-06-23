"""CEFR placement test + level progression engine (Phase 14, rebuilt).

The test mixes authored grammar/vocab MCQs (A1→B2) with three short original
German reading passages (Lesen, easy→hard) plus one free-write prompt. Options
are shuffled before they reach the client (the correct answer is never in a
fixed slot). Objective answers are scored locally; the final CEFR level is
decided by Gemini from that picture + the writing sample (see ai_assistant.llm),
with a graceful fallback to local scoring if AI is unavailable.

All content is original (not from any copyrighted book).
"""

from __future__ import annotations

import random

# Ordered levels the objective items are tagged with.
PLACEMENT_LEVELS = ["A1", "A2", "B1", "B2"]
PASS_RATIO = 0.6  # share of a level's questions needed to "pass" it (local grade)

# --- Grammar / vocabulary MCQs: id, level, prompt, options, answer ---
GRAMMAR_QUESTIONS = [
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
        "id": "a1_4",
        "level": "A1",
        "prompt": "Ich ___ Student.",
        "options": ["bin", "bist", "ist", "sind"],
        "answer": "bin",
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
        "id": "a2_4",
        "level": "A2",
        "prompt": "Ich interessiere mich ___ Musik.",
        "options": ["für", "auf", "an", "über"],
        "answer": "für",
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
        "id": "b1_4",
        "level": "B1",
        "prompt": "Der Film, ___ ich gesehen habe, war gut.",
        "options": ["den", "der", "dem", "dessen"],
        "answer": "den",
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

# --- Reading passages (Lesen): original German, easy→hard, with MCQs ---
READING_PASSAGES = [
    {
        "id": "r_a2",
        "level": "A2",
        "title": "Mein Tag",
        "text": (
            "Hallo! Ich heiße Lena und ich wohne in Hamburg. Morgens trinke ich "
            "Kaffee und fahre mit dem Fahrrad zur Arbeit. Mittags esse ich oft mit "
            "meiner Kollegin. Am Abend lese ich gern ein Buch."
        ),
        "questions": [
            {
                "id": "r_a2_1",
                "prompt": "Wo wohnt Lena?",
                "options": ["In Hamburg", "In Berlin", "In München", "In Köln"],
                "answer": "In Hamburg",
            },
            {
                "id": "r_a2_2",
                "prompt": "Wie fährt Lena zur Arbeit?",
                "options": ["Mit dem Fahrrad", "Mit dem Auto", "Mit dem Bus", "Zu Fuß"],
                "answer": "Mit dem Fahrrad",
            },
            {
                "id": "r_a2_3",
                "prompt": "Was macht Lena am Abend?",
                "options": ["Sie liest ein Buch", "Sie trinkt Kaffee", "Sie arbeitet", "Sie kocht"],
                "answer": "Sie liest ein Buch",
            },
        ],
    },
    {
        "id": "r_b1",
        "level": "B1",
        "title": "Ein Wochenende in den Bergen",
        "text": (
            "Letztes Wochenende sind meine Freunde und ich in die Berge gefahren. "
            "Obwohl das Wetter am Samstag schlecht war, hatten wir viel Spaß. Wir "
            "sind gewandert und haben abends zusammen gekocht. Am Sonntag schien "
            "endlich die Sonne, und wir konnten den See sehen."
        ),
        "questions": [
            {
                "id": "r_b1_1",
                "prompt": "Wann war das Wetter schlecht?",
                "options": ["Am Samstag", "Am Sonntag", "Am Freitag", "Die ganze Zeit"],
                "answer": "Am Samstag",
            },
            {
                "id": "r_b1_2",
                "prompt": "Was haben sie abends gemacht?",
                "options": ["Zusammen gekocht", "Ferngesehen", "Gelesen", "Gearbeitet"],
                "answer": "Zusammen gekocht",
            },
            {
                "id": "r_b1_3",
                "prompt": "Was passierte am Sonntag?",
                "options": ["Die Sonne schien", "Es regnete", "Sie fuhren heim", "Es schneite"],
                "answer": "Die Sonne schien",
            },
        ],
    },
    {
        "id": "r_b2",
        "level": "B2",
        "title": "Sprachen lernen",
        "text": (
            "Viele Menschen glauben, dass man eine Sprache nur in einem Kurs lernen "
            "kann. Tatsächlich spielt jedoch das tägliche Üben eine viel größere "
            "Rolle. Wer regelmäßig liest, hört und spricht, macht oft schnellere "
            "Fortschritte als jemand, der nur einmal pro Woche einen Kurs besucht."
        ),
        "questions": [
            {
                "id": "r_b2_1",
                "prompt": "Was ist laut Text am wichtigsten?",
                "options": ["Tägliches Üben", "Ein teurer Kurs", "Ein Lehrer", "Grammatikbücher"],
                "answer": "Tägliches Üben",
            },
            {
                "id": "r_b2_2",
                "prompt": "Wer macht schnellere Fortschritte?",
                "options": [
                    "Wer regelmäßig übt",
                    "Wer einen Kurs besucht",
                    "Wer viel bezahlt",
                    "Wer im Ausland lebt",
                ],
                "answer": "Wer regelmäßig übt",
            },
            {
                "id": "r_b2_3",
                "prompt": "Das Wort „Fortschritte“ bedeutet …",
                "options": ["Verbesserungen", "Probleme", "Pausen", "Fehler"],
                "answer": "Verbesserungen",
            },
        ],
    },
]

WRITING_PROMPT = {
    "id": "w_1",
    "prompt": "Schreib 1–2 Sätze auf Deutsch: Warum lernst du Deutsch? "
    "(Write 1–2 sentences in German — why are you learning German?)",
}


def _public_question(q: dict, level: str) -> dict:
    """A question safe to send to the client: options shuffled, answer removed."""
    options = list(q["options"])
    random.shuffle(options)
    return {"id": q["id"], "level": level, "prompt": q["prompt"], "options": options}


def public_test() -> dict:
    """The full test payload for the client (shuffled options, no answers)."""
    return {
        "grammar": [_public_question(q, q["level"]) for q in GRAMMAR_QUESTIONS],
        "reading": [
            {
                "id": p["id"],
                "level": p["level"],
                "title": p["title"],
                "text": p["text"],
                "questions": [_public_question(q, p["level"]) for q in p["questions"]],
            }
            for p in READING_PASSAGES
        ],
        "writing": WRITING_PROMPT,
    }


def _answer_key() -> dict[str, dict]:
    """Flat {question_id: {level, answer}} across grammar + reading."""
    key: dict[str, dict] = {}
    for q in GRAMMAR_QUESTIONS:
        key[q["id"]] = {"level": q["level"], "answer": q["answer"]}
    for p in READING_PASSAGES:
        for q in p["questions"]:
            key[q["id"]] = {"level": p["level"], "answer": q["answer"]}
    return key


def score_objective(answers: dict) -> dict:
    """`answers` maps question id -> chosen option. Returns the per-level
    correct/total breakdown plus overall totals."""
    key = _answer_key()
    by_level = {lvl: {"correct": 0, "total": 0} for lvl in PLACEMENT_LEVELS}
    correct = 0
    for qid, meta in key.items():
        bucket = by_level.setdefault(meta["level"], {"correct": 0, "total": 0})
        bucket["total"] += 1
        if str(answers.get(qid, "")).strip() == meta["answer"]:
            bucket["correct"] += 1
            correct += 1
    return {"per_level": by_level, "correct": correct, "total": len(key)}


def local_level(summary: dict) -> str:
    """Fallback level: the highest level passed consecutively from A1 up."""
    suggested = "A1"
    for lvl in PLACEMENT_LEVELS:
        stats = summary["per_level"].get(lvl)
        ratio = (stats["correct"] / stats["total"]) if stats and stats["total"] else 0
        if ratio >= PASS_RATIO:
            suggested = lvl
        else:
            break
    return suggested


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
