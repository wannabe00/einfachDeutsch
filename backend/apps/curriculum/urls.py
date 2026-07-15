from django.urls import path as url_path

from . import views

urlpatterns = [
    url_path("curriculum/path/", views.path, name="curriculum-path"),
    url_path("curriculum/units/<int:unit_id>/", views.unit_detail, name="curriculum-unit"),
]
