from dataclasses import asdict
from django.db import transaction

from apps.audit.context import AuditContext
from apps.accounts.tasks.user_tasks import process_audit_event
from apps.storage.tasks.process_storage_event import process_storage_event

from apps.accounts.events.user_event import (
    UserRegisteredEvent,
    UserLoggedInEvent,
    UserChangedPasswordEvent,
)

from apps.storage.events.storage_event import (
    FileUploadRequestedEvent,
    FileUploadedEvent,
)


class EventBus:

    _routes = {
        UserRegisteredEvent: (
            process_audit_event,
        ),

        UserLoggedInEvent: (
            process_audit_event,
        ),

        UserChangedPasswordEvent: (
            process_audit_event,
        ),

        FileUploadRequestedEvent: (
            process_storage_event,
        ),

        FileUploadedEvent: (
            process_audit_event,
        ),
    }

    @classmethod
    def publish(cls, event):

        payload = asdict(event)
        payload.update(AuditContext.get())

        publishers = cls._routes.get(type(event), ())

        if not publishers:
            return

        def dispatch():
            for publisher in publishers:
                publisher.delay(
                    event_name=type(event).__name__,
                    payload=payload,
                )

        transaction.on_commit(dispatch)