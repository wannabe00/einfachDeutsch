from datetime import date

from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import (
    api_view,
    parser_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.ai_assistant.llm import AIConfigError
from apps.ai_assistant.throttles import AIBurstThrottle, AIDailyThrottle

from .grading import grade_retelling
from .models import RecitationAttempt
from .transcribe import get_transcriber


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([AIBurstThrottle, AIDailyThrottle])
@parser_classes([MultiPartParser, FormParser])
def recite(request):
    """Accept an audio retelling + the source text, transcribe (Gemini, audio
    discarded after), grade it, save the result, and return the feedback card."""
    source_text = (request.data.get("source_text") or "").strip()
    audio = request.FILES.get("audio")
    if not source_text or audio is None:
        return Response({"detail": "Both 'source_text' and 'audio' are required."}, status=400)

    # Size cap (a server-side proxy for length; the client also caps duration).
    max_mb = settings.RECITATION_MAX_AUDIO_MB
    if audio.size > max_mb * 1024 * 1024:
        return Response({"detail": f"Recording too large (max {max_mb} MB)."}, status=400)

    # Per-user daily cap.
    midnight = timezone.make_aware(
        timezone.datetime.combine(date.today(), timezone.datetime.min.time())
    )
    used = RecitationAttempt.objects.filter(user=request.user, created_at__gte=midnight).count()
    cap = settings.RECITATION_DAILY_CAP
    if used >= cap:
        return Response(
            {"detail": f"Daily recitation limit reached ({cap}). Come back tomorrow."},
            status=429,
        )

    try:
        transcript = get_transcriber().transcribe(audio.read(), audio.content_type or "audio/webm")
        result = grade_retelling(source_text, transcript)
    except AIConfigError as exc:
        return Response({"detail": str(exc)}, status=503)
    except Exception:  # noqa: BLE001 — any provider/transcription failure
        return Response(
            {"detail": "Could not process the recording. Please try again."},
            status=502,
        )

    attempt = RecitationAttempt.objects.create(
        user=request.user,
        source_text=source_text,
        transcript=transcript,
        coverage_score=result.get("coverage_score"),
        feedback=result,
    )
    return Response({"id": attempt.id, "transcript": transcript, **result})
