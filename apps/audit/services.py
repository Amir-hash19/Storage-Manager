from apps.audit.repositories import AuditRepository





class AuditServices:

    @classmethod
    def handle_event(cls, event_name, payload):

        if event_name == "UserRegisteredEvent":
            AuditRepository.create(
                user_id=payload["user_id"],
                action="REGISTER",
                resource="USER",
                resource_id=payload["user_id"],
                status="SUCCESS",
                metadata={
                    "email": payload["email"],
                    "username": payload["username"],
                },
)

        elif event_name == "UserLoggedInEvent":
                AuditRepository.create(
                user_id=payload["user_id"],
                action="LOGIN",
                resource="USER",
                status="SUCCESS",
                metadata=payload,
            )