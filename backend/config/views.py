"""Project-level views, including the API root."""

from django.contrib import admin
from django.http import HttpResponse
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


def admin_login(request, **kwargs):
    """The admin's login page with the same per-IP attempt limit as the app's
    login (Django's own admin login has none)."""
    from apps.accounts.throttles import LoginThrottle

    if request.method == "POST" and not LoginThrottle().allow_request(request, None):
        return HttpResponse("Too many login attempts. Try again in a minute.", status=429)
    return admin.site.login(request, **kwargs)
