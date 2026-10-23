"""Everything stored about one user, for "Export my data" (the right of
access): every table with a link to the user is found automatically, so new
features are included without changes here. Secrets are left out: login and
OAuth tokens, the password hash, the 2FA secret and backup codes, staff logs."""

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core import serializers
from django.utils import timezone

SKIPPED_MODELS = {
    "admin.logentry",
    "authtoken.token",
    "authtoken.tokenproxy",
    "socialaccount.socialtoken",
}
SECRET_FIELDS = {
    "password",
    "key",
    "token",
    "token_secret",
    "totp_secret",
    "totp_backup_codes",
    "totp_last_step",
    "extra_data",
}
USER_FIELDS = ("username", "email", "first_name", "last_name", "date_joined", "last_login")


def _rows(queryset) -> list[dict]:
    rows = []
    for item in serializers.serialize("python", queryset):
        fields = {k: v for k, v in item["fields"].items() if k not in SECRET_FIELDS}
        rows.append({"id": item["pk"], **fields})
    return rows


def user_data(user) -> dict:
    User = get_user_model()
    data = {}
    for model in apps.get_models():
        label = model._meta.label_lower
        if label in SKIPPED_MODELS:
            continue
        for field in model._meta.concrete_fields:
            if field.is_relation and field.related_model is User:
                rows = _rows(model.objects.filter(**{field.name: user}))
                if rows:
                    data.setdefault(model._meta.label, []).extend(rows)
    # Chat messages belong to a conversation, not directly to the user.
    from apps.ai_assistant.models import Message

    messages = _rows(Message.objects.filter(conversation__user=user).order_by("created_at"))
    if messages:
        data["ai_assistant.Message"] = messages
    return {
        "exported_at": timezone.now(),
        "account": {name: getattr(user, name) for name in USER_FIELDS},
        "data": data,
    }
