from django.urls import path

from . import views

urlpatterns = [
    path("talk/", views.history, name="talk-history"),
    path("talk/start/", views.start, name="talk-start"),
    path("talk/remove/", views.remove, name="talk-remove"),
    path("talk/<int:talk_id>/", views.detail, name="talk-detail"),
    path("talk/<int:talk_id>/finish/", views.finish, name="talk-finish"),
]
