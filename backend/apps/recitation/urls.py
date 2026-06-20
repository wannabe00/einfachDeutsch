from django.urls import path

from . import views

urlpatterns = [
    path("recitation/attempt/", views.recite, name="recitation-attempt"),
]
