"""Quiz helpers shared by the built-in and the AI-written history lessons.

A quiz is stored WITH answers as [{"prompt", "options", "answer"}]. The client
only ever gets prompts and options, shuffled the same way every time for a
given lesson (the content lists the right answer first).
"""

import random


def public_quiz(quiz: list[dict], seed: str) -> list[dict]:
    out = []
    for i, q in enumerate(quiz or []):
        options = list(q.get("options", []))
        random.Random(f"{seed}-{i}").shuffle(options)
        out.append({"id": i, "prompt": q.get("prompt", ""), "options": options})
    return out


def grade_quiz(quiz: list[dict], answers: dict) -> dict:
    """Grade `answers` ({question index: chosen option}) against the quiz."""
    results, correct = [], 0
    for i, q in enumerate(quiz or []):
        chosen = str(answers.get(str(i), answers.get(i, ""))).strip()
        ok = chosen == str(q.get("answer", "")).strip()
        correct += ok
        results.append({"id": i, "correct": ok, "answer": q.get("answer", "")})
    total = len(quiz or [])
    score = round(correct / total * 100) if total else 100
    return {"score": score, "correct": correct, "total": total, "results": results}
