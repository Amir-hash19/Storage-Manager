from dataclasses import asdict
from apps.accounts.tasks.user_tasks import process_audit_event
from apps.audit.context import AuditContext




class EventBus:

    @staticmethod
    def publish(event):

        payload = asdict(event)

        payload.update(AuditContext.get())


        process_audit_event.delay(
            event_name=event.__class__.__name__,
            payload=payload,
        )