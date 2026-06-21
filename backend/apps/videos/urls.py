from django.urls import path

from . import views

urlpatterns = [
    path("videos/", views.suggestions, name="video-suggestions"),
]
