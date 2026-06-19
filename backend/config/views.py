"""Project-level views, including the API root."""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    """Entry point for the browsable API.

    App endpoints are registered here as their bricks land
    (books in Phase 2, vocabulary in Phase 3, etc.).
    """
    return Response(
        {
            "message": "German Learning Platform API",
            "endpoints": {
                "books": reverse("book-list", request=request, format=format),
            },
        }
    )
