from django.conf import settings
from django.core.mail import send_mail





class EmailService:

    _handlers = {
        "PasswordResetRequestedEvent": "_handle_password_reset_requested",
    }

    @classmethod
    def handle_event(cls, event_name: str, payload: dict):

        handler_name = cls._handlers.get(event_name)

        if handler_name is None:
            return

        handler = getattr(cls, handler_name)

        handler(payload)

    @staticmethod
    def _handle_password_reset_requested(payload):

        reset_link = (
            f"{settings.FRONTEND_URL}/reset-password"
            f"?token={payload['token']}"
        )

        send_mail(
            subject="Reset Password",
            message=(
                "For Changing password press this link.\n\n"
                f"{reset_link}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[payload["email"]],
        )