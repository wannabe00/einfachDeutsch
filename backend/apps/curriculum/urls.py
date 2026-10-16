from django.urls import path as url_path

from . import views

urlpatterns = [
    url_path("curriculum/energy/", views.energy, name="curriculum-energy"),
    url_path("curriculum/gamification/", views.gamification, name="curriculum-gamification"),
    # Level checkpoint exam.
    url_path("curriculum/exam/", views.exam_status, name="curriculum-exam"),
    url_path("curriculum/exam/start/", views.exam_start, name="curriculum-exam-start"),
    url_path("curriculum/exam/submit/", views.exam_submit, name="curriculum-exam-submit"),
    url_path("curriculum/path/", views.path, name="curriculum-path"),
    # Practice sets from finished lessons.
    url_path("curriculum/practice/", views.practice_options, name="curriculum-practice"),
    url_path("curriculum/practice/start/", views.practice_start, name="curriculum-practice-start"),
    url_path(
        "curriculum/practice/answer/", views.practice_answer, name="curriculum-practice-answer"
    ),
    # Checks: reviews of finished Lektionen and Modul tests.
    url_path("curriculum/checks/", views.checks_status, name="curriculum-checks"),
    url_path("curriculum/checks/start/", views.check_start, name="curriculum-check-start"),
    url_path("curriculum/checks/<int:check_id>/", views.check_detail, name="curriculum-check"),
    url_path(
        "curriculum/checks/<int:check_id>/answer/",
        views.check_answer,
        name="curriculum-check-answer",
    ),
    url_path(
        "curriculum/checks/<int:check_id>/finish/",
        views.check_finish,
        name="curriculum-check-finish",
    ),
    url_path("curriculum/lesen/", views.lesen_status, name="curriculum-lesen"),
    url_path(
        "curriculum/lesen/<str:level>/<int:modul>/", views.lesen_set, name="curriculum-lesen-set"
    ),
    url_path(
        "curriculum/lesen/teil/<int:exercise_id>/answer/",
        views.lesen_answer,
        name="curriculum-lesen-answer",
    ),
    url_path("curriculum/schreiben/", views.schreiben_status, name="curriculum-schreiben"),
    url_path(
        "curriculum/schreiben/<str:level>/<int:modul>/",
        views.schreiben_set,
        name="curriculum-schreiben-set",
    ),
    url_path(
        "curriculum/schreiben/teil/<int:exercise_id>/form/",
        views.schreiben_form,
        name="curriculum-schreiben-form",
    ),
    url_path(
        "curriculum/schreiben/teil/<int:exercise_id>/write/",
        views.schreiben_write,
        name="curriculum-schreiben-write",
    ),
    url_path(
        "curriculum/schreiben/teil/<int:exercise_id>/attempts/",
        views.schreiben_attempts,
        name="curriculum-schreiben-attempts",
    ),
    url_path(
        "curriculum/schreiben/attempts/<int:attempt_id>/self/",
        views.schreiben_self_check,
        name="curriculum-schreiben-self",
    ),
    url_path(
        "curriculum/schreiben/attempts/<int:attempt_id>/ai/",
        views.schreiben_ai_grade,
        name="curriculum-schreiben-ai",
    ),
    url_path("curriculum/units/<int:unit_id>/", views.unit_detail, name="curriculum-unit"),
    url_path("curriculum/lessons/<int:lesson_id>/", views.lesson_detail, name="curriculum-lesson"),
    url_path(
        "curriculum/lessons/<int:lesson_id>/answer/",
        views.lesson_answer,
        name="curriculum-lesson-answer",
    ),
    url_path(
        "curriculum/lessons/<int:lesson_id>/restart/",
        views.lesson_restart,
        name="curriculum-lesson-restart",
    ),
    url_path(
        "curriculum/lessons/<int:lesson_id>/complete/",
        views.lesson_complete,
        name="curriculum-lesson-complete",
    ),
]
