from dataclasses import asdict
from apps.accounts.tasks.user_tasks import process_audit_event, process_email_event
from apps.audit.context import AuditContext
from django.db import transaction




class EventBus:

    _publishers = (
        process_audit_event,
        process_email_event,
    )

    @classmethod
    def publish(cls, event):

        payload = asdict(event)
        payload.update(AuditContext.get())

        def dispatch():
            for publisher in cls._publishers:
                publisher.delay(
                    event_name=event.__class__.__name__,
                    payload=payload,
                )

        transaction.on_commit(dispatch)