"""Project-level views, including the API root."""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    """Landing page of DRF's browsable API."""
    return Response(
        {
            "message": "einfachDeutsch API",
            "endpoints": {
                "books": reverse("book-list", request=request, format=format),
            },
        }
    )
