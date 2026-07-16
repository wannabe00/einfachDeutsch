"""Conversation endpoints (Phase 23.13).

ChatGPT-style history for the AI Assistant: list / new / resume / rename /
delete, with both turns persisted server-side so a chat survives a refresh.

Every view scopes to `request.user`, so one user can never read or touch
another's conversations. Premium-gated + throttled like the rest of AI.
"""

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from . import llm
from .models import Conversation, Message
from .serializers import (
    ConversationDetailSerializer,
    ConversationListSerializer,
    MessageSerializer,
)
from .views import _AI_PERMISSIONS, _AI_THROTTLES

# History replayed into the model. Caps the prompt (cost + latency) while
# keeping enough for the thread to feel continuous.
HISTORY_TURNS = 20


def _own(request, pk) -> Conversation:
    """A conversation belonging to the requesting user, or 404."""
    return get_object_or_404(Conversation, pk=pk, user=request.user)


@api_view(["GET", "POST"])
@permission_classes(_AI_PERMISSIONS)
def conversations(request):
    """GET: the user's conversations, most recent first. POST: start a new one."""
    if request.method == "POST":
        convo = Conversation.objects.create(user=request.user)
        return Response(ConversationDetailSerializer(convo).data, status=status.HTTP_201_CREATED)

    qs = Conversation.objects.filter(user=request.user)
    return Response(ConversationListSerializer(qs, many=True).data)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes(_AI_PERMISSIONS)
def conversation_detail(request, pk: int):
    """GET: the full thread. PATCH: rename. DELETE: remove it (cascades)."""
    convo = _own(request, pk)

    if request.method == "DELETE":
        convo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == "PATCH":
        title = str(request.data.get("title", "")).strip()
        if not title:
            return Response({"detail": "Title can't be empty."}, status=status.HTTP_400_BAD_REQUEST)
        convo.title = title[:120]
        convo.save(update_fields=["title", "updated_at"])

    return Response(ConversationDetailSerializer(convo).data)


@api_view(["POST"])
@permission_classes(_AI_PERMISSIONS)
@throttle_classes(_AI_THROTTLES)
def conversation_messages(request, pk: int):
    """Send a message: persist it, answer with the thread as context, persist the
    reply. Returns both turns so the client doesn't need to re-fetch."""
    convo = _own(request, pk)
    text = str(request.data.get("message", "")).strip()
    if not text:
        return Response({"detail": "Message can't be empty."}, status=status.HTTP_400_BAD_REQUEST)

    # Prior turns become the model's context (before saving the new message, so
    # it isn't duplicated — llm.chat takes it as the separate `message` arg).
    history = [
        {"role": m.role, "content": m.content}
        for m in convo.messages.all().order_by("-created_at", "-id")[:HISTORY_TURNS][::-1]
    ]

    try:
        reply = llm.chat(text, history)
    except llm.AIConfigError as exc:
        # Don't persist a half turn if the model is unavailable.
        return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    user_msg = Message.objects.create(conversation=convo, role=Message.Role.USER, content=text)
    ai_msg = Message.objects.create(conversation=convo, role=Message.Role.ASSISTANT, content=reply)

    convo.apply_auto_title(text)
    convo.save()  # also refreshes updated_at, re-ordering the sidebar

    return Response(
        {
            "conversation": ConversationListSerializer(convo).data,
            "messages": MessageSerializer([user_msg, ai_msg], many=True).data,
        },
        status=status.HTTP_201_CREATED,
    )
