from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.grammar.models import GrammarRule
from apps.vocabulary.models import Word

from . import energy as energy_lib
from . import exam as exam_lib
from . import gating, grading
from .models import Lesson, LessonItem, PathLessonProgress, Unit
from .serializers import (
    LessonDetailSerializer,
    PathUnitSerializer,
    UnitGrammarSerializer,
    UnitWordSerializer,
)


def _energy_payload(user) -> dict:
    """The shared energy shape (Spec v3). Premium users are unlimited, so the
    client shows ∞ and never a countdown."""
    return {
        "current": energy_lib.current_energy(user),
        "max": energy_lib.ENERGY_MAX,
        "premium": user.profile.has_premium,
        "seconds_until_next": energy_lib.seconds_until_next(user),
        "refill_hours": energy_lib.ENERGY_REFILL_HOURS,
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def energy(request):
    """Live energy (Phase 23.6) — polled by the global meter so it can tick and
    refill without loading the whole path. Regen is computed on read, so there's
    no background job."""
    return Response(_energy_payload(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def path(request):
    """The user's learning path (Phase 23.4).

    Level-gated per Spec v3: only units **at or below** the user's level are
    returned — forward-level content is never exposed, not even locked. Within
    the user's own level the path is strictly linear; below it, everything is
    open as optional review.
    """
    user = request.user
    level = user.profile.cefr_level

    units = (
        Unit.objects.filter(cefr_level__in=gating.visible_levels(level))
        .order_by("cefr_level", "order")
        .prefetch_related("lessons")
    )

    states, next_lesson = gating.path_states(user, units)
    crowns = dict(PathLessonProgress.objects.filter(user=user).values_list("lesson_id", "crown"))

    # Attach the computed state/crown so the serializer can read them.
    for unit in units:
        for lesson in unit.lessons.all():
            lesson.state = states.get(lesson.id, "locked")
            lesson.crown = crowns.get(lesson.id, 0)

    return Response(
        {
            "level": level,
            "energy": _energy_payload(user),
            "next_up": (
                {
                    "lesson_id": next_lesson.id,
                    "lesson_title": next_lesson.title,
                    "unit_title": next_lesson.unit.title,
                }
                if next_lesson
                else None
            ),
            "units": PathUnitSerializer(units, many=True).data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unit_detail(request, unit_id: int):
    """One unit's page (Phase 23.4b): its lesson trail + review material.

    Review material comes from the unit's chapter — i.e. the whole Lektion's
    Wortschatz/grammar — so the panel is complete rather than only the handful
    of words its lessons happen to reference. Level-gated: a unit above the
    user's level is refused.
    """
    user = request.user
    unit = get_object_or_404(Unit.objects.prefetch_related("lessons"), pk=unit_id)

    if not gating.is_level_visible(user.profile.cefr_level, unit.cefr_level):
        raise PermissionDenied("This unit is above your level.")

    states, _ = gating.path_states(user, [unit])
    crowns = dict(PathLessonProgress.objects.filter(user=user).values_list("lesson_id", "crown"))
    for lesson in unit.lessons.all():
        lesson.state = states.get(lesson.id, "locked")
        lesson.crown = crowns.get(lesson.id, 0)

    # Prefer the unit's chapter (the whole Lektion's Wortschatz/grammar) so the
    # review panel is complete; fall back to whatever its lessons reference.
    if unit.chapter_id:
        words = Word.objects.filter(chapter_id=unit.chapter_id)
        rules = GrammarRule.objects.filter(chapter_id=unit.chapter_id)
    else:
        items = LessonItem.objects.filter(lesson__unit=unit)
        words = Word.objects.filter(
            id__in=items.exclude(word=None).values_list("word_id", flat=True)
        )
        rules = GrammarRule.objects.filter(
            id__in=items.exclude(grammar_rule=None).values_list("grammar_rule_id", flat=True)
        )

    data = PathUnitSerializer(unit).data
    data["words"] = UnitWordSerializer(words.order_by("id"), many=True).data
    data["grammar"] = UnitGrammarSerializer(rules.order_by("id"), many=True).data
    return Response(data)


# A lesson counts as passed at 60% of its gradable items.
PASS_THRESHOLD = 0.6


def _get_playable_lesson(user, lesson_id: int) -> Lesson:
    """Fetch a lesson the user is actually allowed to play."""
    lesson = get_object_or_404(
        Lesson.objects.select_related("unit").prefetch_related("items"), pk=lesson_id
    )
    if not gating.is_lesson_unlocked(user, lesson):
        raise PermissionDenied("This lesson is locked.")
    return lesson


def _already_completed(user, lesson: Lesson) -> bool:
    return PathLessonProgress.objects.filter(
        user=user, lesson=lesson, completed_at__isnull=False
    ).exists()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def lesson_detail(request, lesson_id: int):
    """A lesson's playable items (Phase 23.5), answers stripped.

    Free users need energy to start a **new** lesson; redoing a completed one is
    always free (Spec v3), as is Review/Word Bank/Grammar.
    """
    user = request.user
    lesson = _get_playable_lesson(user, lesson_id)

    is_new = not _already_completed(user, lesson)
    if is_new and not user.profile.has_premium and energy_lib.current_energy(user) < 1:
        return Response(
            {
                "detail": "Out of energy.",
                "seconds_until_next": energy_lib.seconds_until_next(user),
            },
            status=status.HTTP_402_PAYMENT_REQUIRED,
        )

    data = LessonDetailSerializer(lesson).data
    data["is_new"] = is_new
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def lesson_answer(request, lesson_id: int):
    """Grade a single item for immediate feedback. Records nothing — the
    authoritative scoring happens in `lesson_complete`."""
    user = request.user
    lesson = _get_playable_lesson(user, lesson_id)

    item = get_object_or_404(LessonItem, pk=request.data.get("item_id"), lesson=lesson)
    if not item.exercise_id:
        return Response({"detail": "This item isn't gradable."}, status=status.HTTP_400_BAD_REQUEST)

    correct = grading.grade(item.exercise, request.data.get("answer"))
    return Response(
        {
            "correct": correct,
            "solution": grading.solution_of(item.exercise),
            "explanation": item.exercise.explanation,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def lesson_complete(request, lesson_id: int):
    """Finish a lesson: re-grade every answer server-side, then award.

    Energy is spent **on a successful first completion** only — quitting costs
    nothing and a failed attempt doesn't advance the path (Spec v3).
    """
    user = request.user
    lesson = _get_playable_lesson(user, lesson_id)

    submitted = {a.get("item_id"): a.get("answer") for a in request.data.get("answers", [])}
    gradable = [i for i in lesson.items.all() if i.exercise_id]
    correct_count = sum(1 for i in gradable if grading.grade(i.exercise, submitted.get(i.id)))
    score = (correct_count / len(gradable)) if gradable else 1.0
    passed = score >= PASS_THRESHOLD

    was_completed = _already_completed(user, lesson)
    progress, _ = PathLessonProgress.objects.get_or_create(user=user, lesson=lesson)
    progress.best_score = max(progress.best_score or 0.0, score)

    spent_energy = False
    if passed and not was_completed:
        # First real completion: this is what costs energy.
        if not energy_lib.consume(user):
            return Response(
                {
                    "detail": "Out of energy.",
                    "seconds_until_next": energy_lib.seconds_until_next(user),
                },
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )
        spent_energy = not user.profile.has_premium
        progress.completed_at = timezone.now()
        progress.crown = max(progress.crown, 1)
        progress.xp_earned = lesson.xp_reward
    progress.save()

    return Response(
        {
            "passed": passed,
            "score": round(score, 3),
            "correct": correct_count,
            "total": len(gradable),
            "xp_earned": lesson.xp_reward if (passed and not was_completed) else 0,
            "crown": progress.crown,
            "spent_energy": spent_energy,
            "energy": _energy_payload(user),
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def exam_status(request):
    """Progress toward the level checkpoint exam, and whether it's unlocked."""
    return Response(exam_lib.exam_status(request.user))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def exam_start(request):
    """Open an attempt. The sampled questions are frozen on the attempt."""
    try:
        attempt, questions = exam_lib.start_attempt(request.user)
    except exam_lib.ExamError as err:
        return Response({"detail": str(err)}, status=status.HTTP_403_FORBIDDEN)
    return Response({"attempt_id": attempt.id, "questions": questions})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def exam_submit(request):
    """Grade the attempt and promote on a pass."""
    try:
        result = exam_lib.submit_attempt(
            request.user,
            request.data.get("attempt_id"),
            request.data.get("answers") or {},
        )
    except exam_lib.ExamError as err:
        return Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(result)
