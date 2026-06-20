from django.urls import path

from . import views

urlpatterns = [
    path("accounts/set-level/", views.set_level, name="set-level"),
    path("accounts/placement-test/", views.placement_test, name="placement-test"),
    path("accounts/level-status/", views.level_status, name="level-status"),
    path("accounts/streak/", views.streak, name="streak"),
]
