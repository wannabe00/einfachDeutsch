"""Talk to AI (premium): a live spoken conversation with Gemini, then a report.

The browser opens the Live session itself with a short-lived token from
`start` (the API key never leaves the server; model, voice, role and level are
locked into the token). At the end it sends the transcript to `finish`, which
saves it and writes the report. Situations open like Lesen sets.
"""

import random
import unicodedata

from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.levels import level_rank, visible_levels
from apps.accounts.permissions import IsPremium
from apps.ai_assistant import llm
from apps.ai_assistant.throttles import AIBurstThrottle, AIDailyThrottle
from apps.curriculum.learned import finished_units
from apps.curriculum.models import Unit

from .models import Talk

MAX_TURNS = 200
MAX_CHARS = 600
PREMIUM = [IsAuthenticated, IsPremium]
AI_THROTTLES = [AIBurstThrottle, AIDailyThrottle]


TOPICS = 12  # the most recent Lektion themes the AI may offer


def _summary(talk: Talk) -> dict:
    return {
        "id": talk.id,
        "started_at": talk.started_at.isoformat(),
        "ended_at": talk.ended_at.isoformat() if talk.ended_at else None,
        "summary": talk.report.get("summary", ""),
    }


def talks_this_month(user) -> int:
    """Every started talk counts: the server can't see when the browser hangs up,
    so charging per talk (not per minute) leaves nothing to tamper with."""
    month = timezone.localtime().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return Talk.objects.filter(user=user, started_at__gte=month).count()


def _topics(user) -> list[str]:
    """Themes of the Lektionen the user has finished, and of all lower levels."""
    level = user.profile.cefr_level
    lower = [lv for lv in visible_levels(level) if level_rank(lv) < level_rank(level)]
    units = Unit.objects.filter(Q(id__in=finished_units(user)) | Q(cefr_level__in=lower))
    themes = [u.theme for u in sorted(units, key=lambda u: (level_rank(u.cefr_level), u.order))]
    return list(dict.fromkeys(t for t in themes if t))[-TOPICS:]


def _ai_error(fn):
    try:
        return fn()
    except llm.AIConfigError as err:
        return Response({"detail": str(err)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except llm.AIResponseError as err:
        return Response({"detail": f"{err} Please try again."}, status=status.HTTP_502_BAD_GATEWAY)


@api_view(["POST"])
@permission_classes(PREMIUM)
@throttle_classes(AI_THROTTLES)
def start(request):
    """Check the monthly and daily caps, then hand out a Live token for one talk."""
    user = request.user
    level = user.profile.cefr_level
    today = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    if Talk.objects.filter(user=user, started_at__gte=today).count() >= settings.TALK_DAILY_CAP:
        return Response(
            {"detail": f"That's {settings.TALK_DAILY_CAP} talks today. Come back tomorrow!"},
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )
    if talks_this_month(user) >= settings.TALK_MONTHLY_CAP:
        return Response(
            {"detail": f"You've had your {settings.TALK_MONTHLY_CAP} talks this month."},
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    def go():
        opener = random.choice(llm.TALK_OPENERS)
        token = llm.live_token(llm.talk_instruction(level, _topics(user), opener))
        talk = Talk.objects.create(user=user, level=level)
        return Response(
            {"id": talk.id, "token": token, "model": llm.LIVE_MODEL, "minutes": llm.LIVE_MINUTES}
        )

    return _ai_error(go)


def _readable(text: str) -> str:
    """Like the browser: a line with letters outside the Latin alphabet (German and
    English only) is the speech recogniser guessing, so it becomes "(unklar)"."""
    latin = all("LATIN" in unicodedata.name(c, "") for c in text if c.isalpha())
    return text if latin else "(unklar)"


def _clean(transcript) -> list[dict] | None:
    """The transcript as the browser sent it, checked and capped (it's untrusted)."""
    if not isinstance(transcript, list):
        return None
    out = []
    for turn in transcript[:MAX_TURNS]:
        if not isinstance(turn, dict) or turn.get("role") not in ("user", "ai"):
            return None
        text = str(turn.get("text", "")).strip()[:MAX_CHARS]
        if text:
            out.append({"role": turn["role"], "text": _readable(text)})
    return out


@api_view(["POST"])
@permission_classes(PREMIUM)
@throttle_classes(AI_THROTTLES)
def finish(request, talk_id: int):
    """Save the transcript and write the report (a failed report can be retried)."""
    talk = Talk.objects.filter(id=talk_id, user=request.user, removed_at=None).first()
    if talk is None:
        return Response({"detail": "No such talk."}, status=status.HTTP_404_NOT_FOUND)
    if talk.report:
        return Response({"detail": "This talk already has its report."}, status=400)
    transcript = _clean(request.data.get("transcript"))
    if transcript is None:
        return Response({"detail": "The transcript isn't valid."}, status=400)
    talk.transcript = transcript
    talk.ended_at = talk.ended_at or timezone.now()
    talk.save(update_fields=["transcript", "ended_at"])
    if not any(t["role"] == "user" for t in transcript):
        return Response({**_summary(talk), "transcript": transcript, "report": {}})

    def go():
        talk.report = llm.talk_report(talk.level, transcript)
        talk.save(update_fields=["report"])
        return Response({**_summary(talk), "transcript": talk.transcript, "report": talk.report})

    return _ai_error(go)


@api_view(["GET"])
@permission_classes(PREMIUM)
def history(request):
    """The user's own talks, newest first."""
    talks = Talk.objects.filter(user=request.user, ended_at__isnull=False, removed_at=None)[:50]
    return Response([_summary(t) for t in talks])


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove(request):
    """Remove the user's own talks `{ids: [...]}`: the transcript and report are
    deleted for good; an empty row stays so the daily cap still counts it."""
    ids = request.data.get("ids")
    if not isinstance(ids, list) or not all(isinstance(i, int) for i in ids):
        return Response({"detail": "Send the ids of the talks to remove."}, status=400)
    removed = Talk.objects.filter(user=request.user, id__in=ids, removed_at=None).update(
        transcript=[], report={}, removed_at=timezone.now()
    )
    return Response({"removed": removed})


@api_view(["GET"])
@permission_classes(PREMIUM)
def detail(request, talk_id: int):
    talk = Talk.objects.filter(id=talk_id, user=request.user, removed_at=None).first()
    if talk is None:
        return Response({"detail": "No such talk."}, status=status.HTTP_404_NOT_FOUND)
    return Response({**_summary(talk), "transcript": talk.transcript, "report": talk.report})
