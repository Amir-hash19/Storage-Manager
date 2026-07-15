from apps.audit.repositories import AuditRepository
from .constants import AuditAction, AuditResource, AuditStatus


class AuditService:

    _handlers = {
        "UserRegisteredEvent": "_handle_user_registered",
        "UserLoggedInEvent": "_handle_user_logged_in",
        "UserChangedPasswordEvent": "_handle_user_changed_password",
    }


    @classmethod
    def handle_event(cls, event_name: str, payload: dict):

        handle_name = cls._handlers.get(event_name)

        if handle_name is None:
            return 
        
        handler = getattr(cls, handle_name)
        handler(payload)

    @staticmethod
    def _handle_user_registered(payload: dict):
        AuditRepository.create(
            user_id=payload["user_id"],
            action=AuditAction.REGISTER,
            resource="USER",
            resource_id=payload["user_id"],
            status="SUCCESS",

            ip_address=payload.get("ip_address"),
            user_agent=payload.get("user_agent"), 
            request_id=payload.get("request_id"),

            metadata={
                "email": payload["email"],
                "username": payload["username"],
            },
        )

    @staticmethod
    def _handle_user_logged_in(payload: dict):
        AuditRepository.create(
            user_id=payload["user_id"],
            action=AuditAction.LOGIN,
            resource="USER",
            resource_id=payload["user_id"],
            status="SUCCESS",
            metadata=payload,
            ip_address=payload.get("ip_address"),
            user_agent=payload.get("user_agent"), 
            request_id=payload.get("request_id")
            
        )        

    @staticmethod
    def _handle_user_changed_password(payload: dict):
        AuditRepository.create(
            user_id=payload["user_id"],
            action=AuditAction.PASSWORD_CHANGE,
            resource="USER",
            resource_id=payload["user_id"],
            status="SUCCESS",
            ip_address=payload.get("ip_address"),
            user_agent=payload.get("user_agent"), 
            request_id=payload.get("request_id"),
            
            metadata={
                "email": payload["email"],
                "username": payload["username"],
            },
        )    