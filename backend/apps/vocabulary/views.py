from datetime import date

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.exercises.models import Exercise, ExerciseAttempt
from apps.grammar.models import GrammarRule

from .models import ReviewLog, Word, WordProgress
from .serializers import WordProgressSerializer, WordSerializer
from .srs import calculate_next_review


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.select_related("progress", "chapter").all()
    serializer_class = WordSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        chapter = self.request.query_params.get("chapter")
        if chapter:
            qs = qs.filter(chapter_id=chapter)
        return qs

    @action(detail=False, methods=["get"], url_path="due")
    def due(self, request):
        words = (
            Word.objects.select_related("progress", "chapter")
            .filter(progress__next_review__lte=date.today())
            .order_by("progress__next_review")
        )
        chapter = request.query_params.get("chapter")
        if chapter:
            words = words.filter(chapter_id=chapter)
        serializer = self.get_serializer(words, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="due-counts")
    def due_counts(self, request):
        """Count of due words per chapter, plus the overall total."""
        from django.db.models import Count

        rows = (
            Word.objects.filter(progress__next_review__lte=date.today())
            .values("chapter_id")
            .annotate(count=Count("id"))
        )
        per_chapter = {r["chapter_id"]: r["count"] for r in rows}
        return Response({"total": sum(per_chapter.values()), "per_chapter": per_chapter})

    @action(detail=True, methods=["post"], url_path="review")
    def review(self, request, pk=None):
        word = self.get_object()
        quality = int(request.data.get("quality", 0))

        progress = word.progress
        new_reps, new_ef, new_interval, next_review_date = calculate_next_review(
            progress.repetitions,
            progress.ease_factor,
            progress.interval,
            quality,
        )

        from django.utils import timezone

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
        progress.save()

        ReviewLog.objects.create(word=word, quality=quality)

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
    """Aggregate dashboard stats."""

    def get(self, request):
        today = date.today()
        midnight = timezone.make_aware(
            timezone.datetime.combine(today, timezone.datetime.min.time())
        )

        reviewed_today = (
            WordProgress.objects.filter(last_reviewed__gte=midnight).count()
            + ExerciseAttempt.objects.filter(attempted_at__gte=midnight).count()
        )

        return Response(
            {
                "due_today": WordProgress.objects.filter(next_review__lte=today).count(),
                "learned_total": WordProgress.objects.filter(interval__gt=21).count(),
                "reviewed_today": reviewed_today,
                "total_words": Word.objects.count(),
                "total_grammar_rules": GrammarRule.objects.count(),
                "total_exercises": Exercise.objects.count(),
            }
        )


class ActivityView(APIView):
    """Review counts per day for the last 7 days: [{date, count}]."""

    def get(self, request):
        from datetime import timedelta

        today = date.today()
        days = [today - timedelta(days=i) for i in range(6, -1, -1)]

        # Count word reviews + exercise attempts per local day.
        counts = {d: 0 for d in days}
        start = timezone.make_aware(
            timezone.datetime.combine(days[0], timezone.datetime.min.time())
        )
        for log in ReviewLog.objects.filter(reviewed_at__gte=start):
            d = timezone.localtime(log.reviewed_at).date()
            if d in counts:
                counts[d] += 1
        for att in ExerciseAttempt.objects.filter(attempted_at__gte=start):
            d = timezone.localtime(att.attempted_at).date()
            if d in counts:
                counts[d] += 1

        return Response([{"date": d.isoformat(), "count": counts[d]} for d in days])
