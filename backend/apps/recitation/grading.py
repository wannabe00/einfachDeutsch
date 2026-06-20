"""Grade a retelling against the source text (Phase 16.3 + 16.4).

Sends source + transcript to Gemini and asks for structured JSON: content
coverage, missed points, grammar errors (article gender + case especially),
pronunciation flags (proxy from the transcription), and a short summary.
"""

from __future__ import annotations

import json

from django.conf import settings
from google import genai
from google.genai import types

from apps.ai_assistant.llm import MODEL, AIConfigError

GRADER_SYSTEM = (
    "You are a supportive German tutor grading a student's spoken retelling of a "
    "text. The student retells in their own words, so wording will differ — judge "
    "MEANING coverage, not verbatim match. Be encouraging but precise. Pay special "
    "attention to article gender (der/die/das) and grammatical case. Respond in "
    "English except when quoting German."
)

_INSTRUCTIONS = (
    "Return ONLY JSON with exactly these keys:\n"
    '  "coverage_score": integer 0-100 (how much of the source meaning was covered),\n'
    '  "covered": array of short strings (key points the student DID convey),\n'
    '  "missed": array of short strings (key points they MISSED),\n'
    '  "grammar_errors": array of objects {"error": string, "correction": string, '
    '"type": "article"|"case"|"verb"|"word_order"|"other"},\n'
    '  "pronunciation_notes": array of short strings (words that seemed mis-said, '
    "inferred from odd/garbled transcription — may be empty),\n"
    '  "summary": one or two short encouraging sentences.'
)


def grade_retelling(source_text: str, transcript: str) -> dict:
    key = settings.GEMINI_API_KEY
    if not key:
        raise AIConfigError("GEMINI_API_KEY is not set.")
    client = genai.Client(api_key=key)
    prompt = (
        f"SOURCE TEXT:\n{source_text}\n\n"
        f"STUDENT RETELLING (auto-transcribed):\n{transcript}\n\n{_INSTRUCTIONS}"
    )
    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=GRADER_SYSTEM,
            max_output_tokens=1200,
            response_mime_type="application/json",
        ),
    )
    raw = (resp.text or "").strip()
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        data = {}

    score = data.get("coverage_score")
    try:
        score = max(0, min(100, int(score))) if score is not None else None
    except (TypeError, ValueError):
        score = None

    return {
        "coverage_score": score,
        "covered": data.get("covered") or [],
        "missed": data.get("missed") or [],
        "grammar_errors": data.get("grammar_errors") or [],
        "pronunciation_notes": data.get("pronunciation_notes") or [],
        "summary": data.get("summary") or (raw if not data else ""),
    }
