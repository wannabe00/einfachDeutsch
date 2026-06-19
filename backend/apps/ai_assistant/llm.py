"""LLM wrapper for AI features. All prompt-building lives here — views call
these functions, they never build prompts inline (see AGENTS.md).

Provider: Google Gemini (the user supplies a free GEMINI_API_KEY). The key is
read from settings (loaded from backend/.env). If it is missing, calls raise
AIConfigError so views can return a clean 503.
"""

from django.conf import settings
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"
MAX_TOKENS = 1024


class AIConfigError(RuntimeError):
    """Raised when the Gemini API key is not configured."""


def _client() -> genai.Client:
    key = settings.GEMINI_API_KEY
    if not key:
        raise AIConfigError(
            "GEMINI_API_KEY is not set. Add it to backend/.env to enable AI features."
        )
    return genai.Client(api_key=key)


def _complete(system: str, contents, max_tokens: int = MAX_TOKENS) -> str:
    # Bind the client to a local so it isn't garbage-collected mid-request
    # (that closes its underlying httpx client → "client has been closed").
    client = _client()
    resp = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=max_tokens,
        ),
    )
    return (resp.text or "").strip()


TUTOR_SYSTEM = (
    "You are a concise, encouraging German tutor for an English-speaking A1–A2 "
    "learner. Always capitalise German nouns and include their article "
    "(der/die/das). Keep answers focused and practical. Use Markdown."
)


def suggest_words(chapter_title: str, chapter_description: str, count: int = 10) -> str:
    prompt = (
        f"Suggest {count} useful German vocabulary words for a beginner chapter "
        f'titled "{chapter_title}".'
    )
    if chapter_description:
        prompt += f" Chapter focus: {chapter_description}."
    prompt += (
        " Return a Markdown table with columns: German (noun + article), English. "
        "Only single words or short noun phrases — no full sentences."
    )
    return _complete(TUTOR_SYSTEM, prompt)


def explain_grammar(topic: str) -> str:
    prompt = (
        f"Explain this German grammar topic for a beginner: {topic}. "
        "Be brief and clear. Include a short rule, a small table if helpful, and "
        "2–3 example sentences with English translations."
    )
    return _complete(TUTOR_SYSTEM, prompt)


def generate_exercises(chapter_title: str, word_list: str) -> str:
    prompt = (
        f'Create 5 short practice exercises for the chapter "{chapter_title}". '
        f"Use these words where possible: {word_list}. "
        "Mix translation, fill-in-the-blank, and article exercises. "
        "For each, give the prompt and the correct answer on separate lines."
    )
    return _complete(TUTOR_SYSTEM, prompt)


def check_exercise_answer(prompt: str, correct_answer: str, user_answer: str) -> str:
    msg = (
        f"Exercise: {prompt}\n"
        f"Expected answer: {correct_answer}\n"
        f"Student's answer: {user_answer}\n\n"
        "Briefly tell the student if they are right. If wrong or close, explain the "
        "difference in one or two sentences. Be encouraging."
    )
    return _complete(TUTOR_SYSTEM, msg)


def chat(message: str, history: list[dict] | None = None) -> str:
    """history: list of {role: 'user'|'assistant', content: str}."""
    contents = []
    for turn in history or []:
        role = turn.get("role")
        text = turn.get("content", "")
        if role in ("user", "assistant") and text:
            # Gemini uses 'model' for the assistant role.
            gem_role = "model" if role == "assistant" else "user"
            contents.append(types.Content(role=gem_role, parts=[types.Part.from_text(text=text)]))
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=message)]))
    return _complete(TUTOR_SYSTEM, contents)
