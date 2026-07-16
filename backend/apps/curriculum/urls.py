from django.urls import path as url_path

from . import views

urlpatterns = [
    url_path("curriculum/energy/", views.energy, name="curriculum-energy"),
    # Level checkpoint exam (Phase 23.14).
    url_path("curriculum/exam/", views.exam_status, name="curriculum-exam"),
    url_path("curriculum/exam/start/", views.exam_start, name="curriculum-exam-start"),
    url_path("curriculum/exam/submit/", views.exam_submit, name="curriculum-exam-submit"),
    url_path("curriculum/path/", views.path, name="curriculum-path"),
    url_path("curriculum/units/<int:unit_id>/", views.unit_detail, name="curriculum-unit"),
    url_path("curriculum/lessons/<int:lesson_id>/", views.lesson_detail, name="curriculum-lesson"),
    url_path(
        "curriculum/lessons/<int:lesson_id>/answer/",
        views.lesson_answer,
        name="curriculum-lesson-answer",
    ),
    url_path(
        "curriculum/lessons/<int:lesson_id>/complete/",
        views.lesson_complete,
        name="curriculum-lesson-complete",
    ),
]
