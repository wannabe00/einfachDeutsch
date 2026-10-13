"""Create three local test accounts at different points of the A1 path.

    python manage.py seed_test_users --password <password>

  starter  onboarding done, nothing learned yet (only the first lesson open)
  midway   the first half of A1 done: words at mixed strength, 30 days of
           reviews, a 12-day streak, half the history reads, energy 2/3
  full     all of A1 done: most words mastered, 60 days of reviews, a 45-day
           streak, every history read; the A1 exam is unlocked but not taken
           (passing it would promote to A2, which has no content yet)

Re-running deletes and rebuilds these three accounts. Local only: the command
refuses to run unless DEBUG is on, so it never touches production. The password
is an argument so it is never stored in the code.
"""

import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import StreakRecord
from apps.curriculum.learned import learned_word_ids
from apps.curriculum.models import EnergyState, Lesson, PathLessonProgress
from apps.history.models import HistoryLesson, UserHistoryProgress
from apps.vocabulary.models import ReviewLog, Word, WordProgress

User = get_user_model()

# username: (share of A1 lessons done, share of history reads done)
PROFILES = {
    "starter": (0.0, 0.0),
    "midway": (0.5, 0.5),
    "full": (1.0, 1.0),
}


class Command(BaseCommand):
    help = "Create local test users 'starter', 'midway' and 'full' (DEBUG only)."

    def add_arguments(self, parser):
        parser.add_argument("--password", required=True, help="Password for all three users.")

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Refusing to run with DEBUG off: test users are for local use only.")

        rng = random.Random(42)  # same data on every run
        lessons = list(
            Lesson.objects.filter(unit__cefr_level="A1").order_by("unit__order", "order")
        )
        history = list(HistoryLesson.objects.filter(cefr_level="A1").order_by("order"))
        if not lessons:
            raise CommandError("No A1 lessons found. Run `manage.py seed_a1_path` first.")

        with transaction.atomic():
            for username, (lesson_share, history_share) in PROFILES.items():
                User.objects.filter(username=username).delete()
                user = self._create_user(username, options["password"])
                done = lessons[: round(len(lessons) * lesson_share)]
                self._complete_lessons(user, done, rng)
                read = history[: round(len(history) * history_share)]
                self._read_history(user, read, rng)
                if username == "midway":
                    self._study_words(
                        user, rng, mastered=0.25, learning=0.45, due_today=15, days=30
                    )
                    self._streak(user, current=12, longest=18, freezes=1)
                    self._energy(user, 2)
                elif username == "full":
                    self._study_words(user, rng, mastered=0.75, learning=0.25, due_today=8, days=60)
                    self._streak(user, current=45, longest=45, freezes=2)
                    self._energy(user, settings.ENERGY_MAX)
                self.stdout.write(
                    f"  {username:<8} {len(done)}/{len(lessons)} lessons, "
                    f"{len(read)}/{len(history)} history reads"
                )

        self.stdout.write(self.style.SUCCESS("Done. Log in at /login with these usernames."))

    def _create_user(self, username, password):
        user = User.objects.create_user(
            username=username,
            email=f"{username}@example.test",
            password=password,
            first_name=username.capitalize(),
            last_name="Test",
        )
        # The post_save signal created the profile; finish onboarding at A1.
        profile = user.profile
        profile.cefr_level = "A1"
        profile.profile_complete = True
        profile.level_set = True
        profile.save()
        return user

    def _complete_lessons(self, user, lessons, rng):
        """Finish lessons in path order, spread over the past weeks."""
        now = timezone.now()
        span = max(len(lessons), 1)
        PathLessonProgress.objects.bulk_create(
            PathLessonProgress(
                user=user,
                lesson=lesson,
                completed_at=now - timedelta(days=(span - i) * 0.9),
                best_score=round(rng.uniform(0.7, 1.0), 2),
                crown=1,
                xp_earned=lesson.xp_reward,
            )
            for i, lesson in enumerate(lessons)
        )

    def _read_history(self, user, lessons, rng):
        now = timezone.now()
        UserHistoryProgress.objects.bulk_create(
            UserHistoryProgress(
                user=user,
                lesson=lesson,
                score=rng.choice([60, 80, 80, 100, 100]),
                completed_at=now - timedelta(days=len(lessons) - i),
            )
            for i, lesson in enumerate(lessons)
        )

    def _study_words(self, user, rng, *, mastered, learning, due_today, days):
        """Review history for the learned words: some mastered (SM-2 interval
        over 21 days), some still learning, a few due today, the rest new.
        Reviews fall on every one of the last `days` days, so the streak and
        the activity chart agree."""
        now = timezone.now()
        word_ids = sorted(learned_word_ids(user))
        rng.shuffle(word_ids)
        words = Word.objects.in_bulk(word_ids)
        n_mastered = round(len(word_ids) * mastered)
        n_learning = round(len(word_ids) * learning)

        progress = []
        for i, word_id in enumerate(word_ids[: n_mastered + n_learning]):
            is_mastered = i < n_mastered
            interval = rng.randint(25, 60) if is_mastered else rng.randint(1, 14)
            due = i >= n_mastered + n_learning - due_today
            last = now - timedelta(days=rng.randint(1, min(interval, days)))
            seen = rng.randint(4, 9) if is_mastered else rng.randint(1, 4)
            wrong = rng.randint(0, 1 if is_mastered else 2)
            progress.append(
                WordProgress(
                    user=user,
                    word=words[word_id],
                    repetitions=seen - wrong,
                    ease_factor=round(rng.uniform(2.3, 2.8), 2),
                    interval=interval,
                    next_review=now.date() if due else (last + timedelta(days=interval)).date(),
                    last_reviewed=last,
                    times_seen=seen,
                    times_correct=seen - wrong,
                    times_wrong=wrong,
                    lapses=wrong,
                )
            )
        # next_review is auto_now_add (forced to today on create), so remember the
        # intended dates and write them back after the insert.
        intended = [p.next_review for p in progress]
        created_progress = WordProgress.objects.bulk_create(progress)
        for row, next_review in zip(created_progress, intended, strict=True):
            row.next_review = next_review
        WordProgress.objects.bulk_update(created_progress, ["next_review"], batch_size=500)

        studied = [p.word for p in progress]
        logs, log_days = [], []
        for day in range(days):
            for word in rng.sample(studied, min(len(studied), rng.randint(6, 24))):
                logs.append(ReviewLog(user=user, word=word, quality=rng.choice([2, 4, 4, 5, 5])))
                log_days.append(day)
        created = ReviewLog.objects.bulk_create(logs)
        # reviewed_at is set automatically on create, so backdate it afterwards,
        # one update per day (0 = today).
        per_day: dict[int, list[int]] = {}
        for log, day in zip(created, log_days, strict=True):
            per_day.setdefault(day, []).append(log.pk)
        for day, pks in per_day.items():
            ReviewLog.objects.filter(pk__in=pks).update(
                reviewed_at=now - timedelta(days=day, hours=rng.randint(0, 6))
            )

    def _streak(self, user, *, current, longest, freezes):
        StreakRecord.objects.update_or_create(
            user=user,
            defaults={
                "current_streak": current,
                "longest_streak": longest,
                "freeze_tokens_available": freezes,
                "last_active_date": timezone.localdate(),
            },
        )

    def _energy(self, user, balance):
        EnergyState.objects.update_or_create(
            user=user, defaults={"balance": balance, "last_refill_at": timezone.now()}
        )
