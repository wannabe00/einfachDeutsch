from django.urls import path as url_path

from . import views

urlpatterns = [
    url_path("curriculum/energy/", views.energy, name="curriculum-energy"),
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
