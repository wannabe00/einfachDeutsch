from datetime import date

from django.db.models import Count, Prefetch, Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.levels import visible_levels_for
from apps.exercises.models import Exercise, ExerciseAttempt
from apps.grammar.models import GrammarRule

from .models import ReviewLog, Word, WordProgress
from .serializers import WordProgressSerializer, WordSerializer
from .srs import calculate_next_review


def current_user(request):
    """The authenticated user, or None for a guest."""
    return request.user if request.user.is_authenticated else None


def _record_activity(user):
    """Update the user's streak — best-effort, never breaks the request."""
    try:
        from apps.accounts.scheduling import register_activity

        register_activity(user)
    except Exception:  # noqa: BLE001 — streak is non-critical
        pass


def locked_chapter_ids_for(user) -> set[int]:
    """Chapters whose vocabulary is still locked for `user` (Phase 23.9).

    A Lektion at the user's **own** level stays locked until they've completed a
    lesson in it — that's what "words from unreached lessons" means. Lektionen
    *below* their level are optional review and always open, and chapters with no
    path unit (legacy content, words the user added) are never locked.

    (Words above the user's level aren't locked — they're not returned at all;
    see the ≤-level filter.)
    """
    if user is None:
        return set()

    # Imported here so the vocabulary app doesn't hard-depend on curriculum.
    from apps.curriculum.models import PathLessonProgress, Unit

    level = user.profile.cefr_level
    reached_unit_ids = set(
        PathLessonProgress.objects.filter(user=user, completed_at__isnull=False).values_list(
            "lesson__unit_id", flat=True
        )
    )
    return set(
        Unit.objects.filter(cefr_level=level, chapter__isnull=False)
        .exclude(id__in=reached_unit_ids)
        .values_list("chapter_id", flat=True)
    )


def due_words_for(user, chapter_id=None):
    """Words due for review for `user`.

    A word is due if the user has a progress row scheduled on/before today, OR
    the user has never reviewed it (new words are due). For a guest (user=None)
    every word is new, so all words are due.

    Level-gated (Spec v3): review never surfaces words above the user's level —
    otherwise forward content would leak in through the back door.
    """
    today = date.today()
    qs = Word.objects.select_related("chapter")
    qs = qs.filter(chapter__cefr_level__in=visible_levels_for(user))
    if chapter_id:
        qs = qs.filter(chapter_id=chapter_id)
    if user is None:
        return qs
    seen = WordProgress.objects.filter(user=user).values("word_id")
    due_seen = WordProgress.objects.filter(user=user, next_review__lte=today).values("word_id")
    return qs.filter(Q(pk__in=due_seen) | ~Q(pk__in=seen))


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.select_related("chapter").all()
    serializer_class = WordSerializer

    def get_permissions(self):
        # Content edits require an account; reading + (guest-safe) review do not.
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
            "import_csv",
            "bulk",
        }:
            return [IsAuthenticated()]
        return [AllowAny()]

    def _with_user_progress(self, qs):
        """Attach the requesting user's progress to each word as `user_progress`
        (a list of 0 or 1 WordProgress) so the serializer avoids an N+1."""
        user = current_user(self.request)
        if user is not None:
            qs = qs.prefetch_related(
                Prefetch(
                    "progress_records",
                    queryset=WordProgress.objects.filter(user=user),
                    to_attr="user_progress",
                )
            )
        return qs

    def get_queryset(self):
        qs = Word.objects.select_related("chapter")
        # ≤-level rule (Spec v3): never expose vocabulary above the user's level.
        # Guests see the lowest level only.
        qs = qs.filter(chapter__cefr_level__in=visible_levels_for(self.request.user))
        chapter = self.request.query_params.get("chapter")
        if chapter:
            qs = qs.filter(chapter_id=chapter)
        return self._with_user_progress(qs)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["locked_chapter_ids"] = locked_chapter_ids_for(current_user(self.request))
        return ctx

    @action(detail=False, methods=["get"], url_path="due")
    def due(self, request):
        user = current_user(request)
        chapter = request.query_params.get("chapter")
        words = self._with_user_progress(due_words_for(user, chapter))
        serializer = self.get_serializer(words, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="due-counts")
    def due_counts(self, request):
        """Count of due words per chapter, plus the overall total."""
        user = current_user(request)
        rows = due_words_for(user).values("chapter_id").annotate(count=Count("id"))
        per_chapter = {r["chapter_id"]: r["count"] for r in rows}
        return Response({"total": sum(per_chapter.values()), "per_chapter": per_chapter})

    @action(detail=True, methods=["post"], url_path="review")
    def review(self, request, pk=None):
        word = self.get_object()
        quality = int(request.data.get("quality", 0))
        user = current_user(request)

        if user is None:
            # Guest: compute the next SM-2 state for display but don't persist it
            # (progress is account-only). Starts from defaults each time.
            progress = WordProgress(word=word)
        else:
            progress, _ = WordProgress.objects.get_or_create(user=user, word=word)

        new_reps, new_ef, new_interval, next_review_date = calculate_next_review(
            progress.repetitions,
            progress.ease_factor,
            progress.interval,
            quality,
        )

        progress.repetitions = new_reps
        progress.ease_factor = new_ef
        progress.interval = new_interval
        progress.next_review = next_review_date
        progress.last_reviewed = timezone.now()
        progress.times_seen += 1
        if quality == 0:
            progress.times_wrong += 1
            progress.lapses += 1
        else:
            progress.times_correct += 1

        if user is not None:
            progress.save()
            ReviewLog.objects.create(word=word, quality=quality, user=user)
            _record_activity(user)

        return Response(WordProgressSerializer(progress).data)

    @action(detail=False, methods=["post"], url_path="import")
    def import_csv(self, request):
        """Bulk-create words from an uploaded CSV (columns: english, german, notes).

        Skips rows where a Word with the same english+chapter already exists.
        """
        import csv
        import io

        file = request.FILES.get("file")
        chapter_id = request.data.get("chapter_id")
        if not file or not chapter_id:
            return Response(
                {"detail": "Both 'file' and 'chapter_id' are required."},
                status=400,
            )

        decoded = file.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(decoded))
        created, skipped = 0, 0
        for row in reader:
            english = (row.get("english") or "").strip()
            german = (row.get("german") or "").strip()
            notes = (row.get("notes") or "").strip()
            if not english or not german:
                skipped += 1
                continue
            exists = Word.objects.filter(chapter_id=chapter_id, english__iexact=english).exists()
            if exists:
                skipped += 1
                continue
            Word.objects.create(chapter_id=chapter_id, english=english, german=german, notes=notes)
            created += 1

        return Response({"created": created, "skipped": skipped})

    @action(detail=False, methods=["post"], url_path="bulk")
    def bulk(self, request):
        """Create many words at once from a JSON list.

        Body: {chapter_id, rows: [{german, english, notes?}]}.
        Skips rows duplicating an existing english+chapter. Returns counts.
        """
        chapter_id = request.data.get("chapter_id")
        rows = request.data.get("rows") or []
        if not chapter_id or not isinstance(rows, list):
            return Response({"detail": "chapter_id and a rows list are required."}, status=400)

        created, skipped = 0, 0
        for row in rows:
            german = (row.get("german") or "").strip()
            english = (row.get("english") or "").strip()
            notes = (row.get("notes") or "").strip()
            if not german or not english:
                skipped += 1
                continue
            if Word.objects.filter(chapter_id=chapter_id, english__iexact=english).exists():
                skipped += 1
                continue
            Word.objects.create(chapter_id=chapter_id, english=english, german=german, notes=notes)
            created += 1

        return Response({"created": created, "skipped": skipped})


class StatsView(APIView):
    """Aggregate dashboard stats for the requesting user (per-user progress;
    content totals are global). Guests see content totals with all words counted
    as new/due and zero personal activity."""

    permission_classes = [AllowAny]

    def get(self, request):
        user = current_user(request)
        today = date.today()
        midnight = timezone.make_aware(
            timezone.datetime.combine(today, timezone.datetime.min.time())
        )

        if user is None:
            due_today = Word.objects.count()  # everything is new for a guest
            learned_total = 0
            reviewed_today = 0
        else:
            due_today = due_words_for(user).count()
            learned_total = WordProgress.objects.filter(user=user, interval__gt=21).count()
            reviewed_today = (
                WordProgress.objects.filter(user=user, last_reviewed__gte=midnight).count()
                + ExerciseAttempt.objects.filter(user=user, attempted_at__gte=midnight).count()
            )

        return Response(
            {
                "due_today": due_today,
                "learned_total": learned_total,
                "reviewed_today": reviewed_today,
                "total_words": Word.objects.count(),
                "total_grammar_rules": GrammarRule.objects.count(),
                "total_exercises": Exercise.objects.count(),
            }
        )


class ActivityView(APIView):
    """Review counts per day for the last 7 days: [{date, count}] for the
    requesting user. Guests get all-zero days."""

    permission_classes = [AllowAny]

    def get(self, request):
        from datetime import timedelta

        user = current_user(request)
        today = date.today()
        days = [today - timedelta(days=i) for i in range(6, -1, -1)]
        counts = {d: 0 for d in days}

        if user is not None:
            start = timezone.make_aware(
                timezone.datetime.combine(days[0], timezone.datetime.min.time())
            )
            for log in ReviewLog.objects.filter(user=user, reviewed_at__gte=start):
                d = timezone.localtime(log.reviewed_at).date()
                if d in counts:
                    counts[d] += 1
            for att in ExerciseAttempt.objects.filter(user=user, attempted_at__gte=start):
                d = timezone.localtime(att.attempted_at).date()
                if d in counts:
                    counts[d] += 1

        return Response([{"date": d.isoformat(), "count": counts[d]} for d in days])
