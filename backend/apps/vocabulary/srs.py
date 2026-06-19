from datetime import date, timedelta


def calculate_next_review(
    repetitions: int,
    ease_factor: float,
    interval: int,
    quality: int,
) -> tuple[int, float, int, date]:
    """SM-2 spaced repetition. quality: 0=Again, 2=Hard, 4=Good, 5=Easy."""
    if quality < 3:
        new_reps = 0
        new_interval = 1
    else:
        new_reps = repetitions + 1
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 6
        else:
            new_interval = round(interval * ease_factor)

    new_ef = ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    new_ef = max(1.3, new_ef)

    next_review = date.today() + timedelta(days=new_interval)
    return new_reps, new_ef, new_interval, next_review
