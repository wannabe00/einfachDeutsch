from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(user_logged_in)
def log_session_login(sender, request, user, **kwargs):
    """Session sign-ins are the Django admin's (the app signs in with tokens)."""
    from .audit import audit

    audit("admin_login", request, user=user)
