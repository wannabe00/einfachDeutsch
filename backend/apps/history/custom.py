"""AI-written history lessons: a learner asks for a topic, the AI may ask a
follow-up question, then writes a lesson at the learner's level with a quiz
and a free picture.

The prompts in ai_assistant/llm.py set the rules (only Germany, the
German-speaking countries and the German language; factual; no hate or
denial). This module enforces what can be checked in code, so a misbehaving
model can't put anything else in front of a learner:

  * chat input is limited in length and number of turns
  * a lesson is only saved if the model says it's on topic, its length fits the
    level, and it has exactly five well-formed questions; otherwise it tries
    once more, then gives up
  * each user may create at most HISTORY_AI_DAILY_LIMIT lessons a day
"""

from django.conf import settings
from django.utils import timezone

from apps.accounts.levels import level_rank
from apps.ai_assistant import llm

from .images import find_image
from .models import CustomHistoryLesson

DAILY_LIMIT = getattr(settings, "HISTORY_AI_DAILY_LIMIT", 5)
MAX_MESSAGE_CHARS = 500
MAX_TURNS = 8
# Words in the German text, per writing level (a little looser than the prompt).
WORDS = {"A1": (100, 260), "A2": (160, 360), "B1": (240, 500), "B2": (280, 580)}
ATTEMPTS = 2


class CustomLessonError(Exception):
    """A request we refuse or couldn't fulfil; `status` is the HTTP status."""

    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def writing_level(user) -> str:
    """The level to write at: the user's own, with C1/C2 written as B2."""
    level = user.profile.cefr_level
    return level if level in WORDS else ("B2" if level_rank(level) > level_rank("B2") else "A1")


def guide(messages) -> dict:
    """One turn of the topic chat. Returns {"status", "reply", "topic"}."""
    if not isinstance(messages, list) or not messages or len(messages) > MAX_TURNS:
        raise CustomLessonError("Start a new request.")
    clean = []
    for m in messages:
        role = m.get("role") if isinstance(m, dict) else None
        content = str(m.get("content", "")).strip() if isinstance(m, dict) else ""
        if role not in ("user", "assistant") or not content:
            raise CustomLessonError("Start a new request.")
        if role == "user" and len(content) > MAX_MESSAGE_CHARS:
            raise CustomLessonError(f"Please keep it under {MAX_MESSAGE_CHARS} characters.")
        clean.append({"role": role, "content": content[:2000]})
    if clean[-1]["role"] != "user":
        raise CustomLessonError("Start a new request.")

    try:
        data = llm.history_lesson_guide(clean)
    except ValueError as err:
        raise CustomLessonError("The assistant got confused. Please try again.", 502) from err

    status = data.get("status")
    reply = str(data.get("reply", "")).strip()[:600]
    topic = str(data.get("topic", "")).strip()[:200]
    if status not in ("ask", "ready", "refuse") or not reply or (status == "ready" and not topic):
        raise CustomLessonError("The assistant got confused. Please try again.", 502)
    return {"status": status, "reply": reply, "topic": topic if status == "ready" else ""}


def _clean(text) -> str:
    text = str(text or "").replace("—", ", ").replace("**", "").replace("#", "")
    paragraphs = [" ".join(p.split()) for p in text.split("\n\n")]
    return "\n\n".join(p for p in paragraphs if p)


def _valid_lesson(data: dict, level: str) -> dict | None:
    """The cleaned lesson, or None if it breaks a rule."""
    if data.get("on_topic") is not True:
        return None
    lesson = {
        "title": _clean(data.get("title"))[:200],
        "era": _clean(data.get("era"))[:80],
        "excerpt": _clean(data.get("excerpt"))[:300],
        "body_de": _clean(data.get("body_de")),
        "body_en": _clean(data.get("body_en")),
        "image_query": _clean(data.get("image_query"))[:120],
    }
    low, high = WORDS[level]
    if not lesson["title"] or not lesson["body_en"]:
        return None
    if not low <= len(lesson["body_de"].split()) <= high:
        return None

    quiz = data.get("quiz")
    if not isinstance(quiz, list) or len(quiz) != 5:
        return None
    lesson["quiz"] = []
    for q in quiz:
        if not isinstance(q, dict) or not isinstance(q.get("options"), list):
            return None
        options = [_clean(o)[:200] for o in q["options"]]
        answer = _clean(q.get("answer"))[:200]
        prompt = _clean(q.get("prompt"))[:300]
        if not prompt or len(options) != 4 or len(set(options)) != 4 or answer not in options:
            return None
        lesson["quiz"].append({"prompt": prompt, "options": options, "answer": answer})
    return lesson


def created_today(user) -> int:
    start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    return CustomHistoryLesson.objects.filter(user=user, created_at__gte=start).count()


def create_lesson(user, topic: str) -> CustomHistoryLesson:
    topic = str(topic or "").strip()
    if not topic or len(topic) > 200:
        raise CustomLessonError("Choose a topic first.")
    if created_today(user) >= DAILY_LIMIT:
        raise CustomLessonError(
            f"You can create {DAILY_LIMIT} lessons a day. Come back tomorrow.", 429
        )

    level = writing_level(user)
    lesson = None
    for _ in range(ATTEMPTS):
        try:
            data = llm.write_history_lesson(topic, level)
        except ValueError:
            continue
        if data.get("on_topic") is False:
            raise CustomLessonError(
                "That topic isn't about Germany or the German language, so I can't write it."
            )
        lesson = _valid_lesson(data, level)
        if lesson:
            break
    if lesson is None:
        raise CustomLessonError("I couldn't write a good lesson on that. Try other words.", 502)

    image_url, image_credit = find_image(
        lesson.pop("image_query"), lesson["title"], f"{lesson.get('era', '')} {lesson['title']}"
    )
    return CustomHistoryLesson.objects.create(
        user=user,
        topic=topic,
        cefr_level=level,
        image_url=image_url,
        image_credit=image_credit,
        **lesson,
    )
