from django.conf import settings
from django.http import JsonResponse


class RequestSizeLimitMiddleware:
    """Refuse a request whose declared body is over MAX_REQUEST_BYTES before
    anything reads it, so a huge upload can't fill memory or disk."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            size = int(request.META.get("CONTENT_LENGTH") or 0)
        except ValueError:
            size = 0
        if size > settings.MAX_REQUEST_BYTES:
            return JsonResponse({"detail": "Request too large."}, status=413)
        return self.get_response(request)


class ApiSecurityHeadersMiddleware:
    """Headers for the JSON API (not the admin's HTML pages): a CSP that lets an
    API response do nothing if a browser ever renders it, and no caching of
    signed-in answers on disk or in shared caches."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/api/"):
            response.setdefault(
                "Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'"
            )
            if "HTTP_AUTHORIZATION" in request.META:
                response.setdefault("Cache-Control", "no-store")
        return response
