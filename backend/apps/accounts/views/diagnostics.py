"""Staff-only check of how the server sees the client's address, to set
NUM_PROXIES right on a new host (throttles are keyed on this address)."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle


@api_view(["GET"])
@permission_classes([IsAdminUser])
def client_ip(request):
    return Response(
        {
            "remote_addr": request.META.get("REMOTE_ADDR"),
            "x_forwarded_for": request.META.get("HTTP_X_FORWARDED_FOR"),
            # What the throttles use. It must be your real IP; if it's the host's
            # proxy address, NUM_PROXIES is too low; if a fake header changes
            # it, too high.
            "throttle_ip": AnonRateThrottle().get_ident(request),
        }
    )
