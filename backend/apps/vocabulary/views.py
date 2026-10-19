import random
from datetime import date

from django.db.models import Count, Prefetch, Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.levels import visible_levels_for
from apps.accounts.scheduling import record_activity
from apps.exercises.models import Exercise, ExerciseAttempt
from apps.grammar.models import GrammarRule

from .models import ReviewLog, SavedWord, Word, WordProgress
from .progress import apply_review, record_review
from .serializers import SavedWordSerializer, WordProgressSerializer, WordSerializer

# Words handed to the drills per round of loading.
DRILL_POOL_SIZE = 60


# Correct reviews in a row that make a word "known" (frontend lib/wordStrength.ts).
KNOWN_AFTER = 2


def drill_weight(progress) -> float:
    """How likely a word is to come up in a drill: weak words more, words the
    user has mastered less. A word never reviewed counts as fairly weak."""
    if progress is None:
        return 2.0
    seen = progress.times_seen or 0
    weight = 1.0 + progress.lapses + 2 * (progress.times_wrong / (seen + 1))
    weight += max(0.0, 2.5 - progress.ease_factor) * 2
    if progress.interval > 21:
        weight /= 2
    return weight


def current_user(request):
    """The authenticated user, or None for a guest."""
    return request.user if request.user.is_authenticated else None


def due_words_for(user, chapter_id=None):
    """Words due for review for `user`.

    A word is due if the user has a progress row scheduled on/before today, OR
    the user has never reviewed it (new words are due). Only learned words
    (see curriculum.learned) are ever due, so review never runs ahead of the
    path. A guest (user=None) has learned nothing, so nothing is due.

    Words above the user's level are never due, or review would leak content
    from higher levels.
    """
    today = date.today()
    qs = Word.objects.select_related("chapter").prefetch_related("chapter__units")
    qs = qs.filter(chapter__cefr_level__in=visible_levels_for(user))
    if chapter_id:
        qs = qs.filter(chapter_id=chapter_id)
    if user is None:
        return qs.none()
    # Imported here so the vocabulary app doesn't hard-depend on curriculum.
    from apps.curriculum.learned import learned_word_ids

    qs = qs.filter(id__in=learned_word_ids(user))
    seen = WordProgress.objects.filter(user=user).values("word_id")
    due_seen = WordProgress.objects.filter(user=user, next_review__lte=today).values("word_id")
    return qs.filter(Q(pk__in=due_seen) | ~Q(pk__in=seen))


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.select_related("chapter").all()
    serializer_class = WordSerializer

    def get_permissions(self):
        # Words are shared content, so only staff may change them (a learner's
        # own words are SavedWord). Reading and (guest-safe) review are open.
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
            "import_csv",
            "bulk",
        }:
            return [IsAdminUser()]
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
        qs = Word.objects.select_related("chapter").prefetch_related("chapter__units")
        # ≤-level rule: never expose vocabulary above the user's level.
        # Guests see the lowest level only.
        qs = qs.filter(chapter__cefr_level__in=visible_levels_for(self.request.user))
        user = current_user(self.request)
        if user is not None:
            # Signed-in users only ever see words they've learned.
            from apps.curriculum.learned import learned_word_ids

            qs = qs.filter(id__in=learned_word_ids(user))
        chapter = self.request.query_params.get("chapter")
        if chapter:
            qs = qs.filter(chapter_id=chapter)
        return self._with_user_progress(qs)

    @action(detail=False, methods=["get"], url_path="due")
    def due(self, request):
        user = current_user(request)
        chapter = request.query_params.get("chapter")
        words = self._with_user_progress(due_words_for(user, chapter))
        serializer = self.get_serializer(words, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="drill")
    def drill(self, request):
        """Words for the drills: learned words only, weak ones more often, in
        random order. Guests get a random set from the lowest level."""
        user = current_user(request)
        qs = (
            Word.objects.select_related("chapter")
            .prefetch_related("chapter__units")
            .filter(chapter__cefr_level__in=visible_levels_for(request.user))
        )
        if user is None:
            words = list(qs.order_by("?")[:DRILL_POOL_SIZE])
        else:
            from apps.curriculum.learned import learned_word_ids

            words = list(self._with_user_progress(qs.filter(id__in=learned_word_ids(user))))
            # Weighted sampling without replacement: sort by a random key
            # raised to 1/weight (Efraimidis-Spirakis), keep the top ones.
            words.sort(
                key=lambda w: (
                    random.random() ** (1 / drill_weight(next(iter(w.user_progress), None)))
                ),
                reverse=True,
            )
            words = words[:DRILL_POOL_SIZE]
            random.shuffle(words)
        return Response(self.get_serializer(words, many=True).data)

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
            progress = apply_review(WordProgress(word=word), quality)
        else:
            progress = record_review(user, word, quality)
            record_activity(user)

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
            due_today = words_learned = mastered_total = reviewed_today = 0
        else:
            from apps.curriculum.learned import learned_word_ids

            due_today = due_words_for(user).count()
            # Learned = taught by a finished lesson; mastered = "known" in the
            # Word Bank (right twice in a row).
            words_learned = len(learned_word_ids(user))
            mastered_total = WordProgress.objects.filter(
                user=user, repetitions__gte=KNOWN_AFTER
            ).count()
            reviewed_today = (
                WordProgress.objects.filter(user=user, last_reviewed__gte=midnight).count()
                + ExerciseAttempt.objects.filter(user=user, attempted_at__gte=midnight).count()
            )

        return Response(
            {
                "due_today": due_today,
                "words_learned": words_learned,
                "mastered_total": mastered_total,
                "reviewed_today": reviewed_today,
                "total_words": Word.objects.count(),
                "total_grammar_rules": GrammarRule.objects.count(),
                "total_exercises": Exercise.objects.count(),
            }
        )


class PublicStatsView(APIView):
    """Live content counts for the landing page.

    Each number is a COUNT(*) of real content, so the landing can't overstate
    anything. Public (guests see the landing) and cached for a while, since the
    counts rarely change.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        from django.core.cache import cache

        cached = cache.get("public_stats")
        if cached is not None:
            return Response(cached)

        from apps.exercises.models import Exercise
        from apps.grammar.models import GrammarRule
        from apps.history.models import HistoryLesson
        from apps.videos.models import ShowSuggestion

        data = {
            "words": Word.objects.count(),
            "exercises": Exercise.objects.count(),
            "grammar_topics": GrammarRule.objects.count(),
            "history_reads": HistoryLesson.objects.count(),
            "video_picks": ShowSuggestion.objects.count(),
        }
        cache.set("public_stats", data, 60 * 15)  # 15 min is plenty
        return Response(data)


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


class SavedWordViewSet(viewsets.ModelViewSet):
    """The learner's own words (list, add, edit, delete), only ever their own."""

    serializer_class = SavedWordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return SavedWord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        german = serializer.validated_data["german"]
        if SavedWord.objects.filter(user=self.request.user, german=german).exists():
            raise ValidationError({"german": "You've already saved this word."})
        serializer.save(user=self.request.user)
