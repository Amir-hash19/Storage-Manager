import uuid
from apps.audit.context import AuditContext


class AuditContextMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        AuditContext.set({
            "ip_address": self.get_client_ip(request),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
            "request_id": str(uuid.uuid4()),
        })

        response = self.get_response(request)

        AuditContext.clear()

        return response

    def get_client_ip(self, request):

        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

        if forwarded:
            return forwarded.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR")