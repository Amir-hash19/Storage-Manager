from dataclasses import asdict
from apps.accounts.tasks.user_tasks import process_audit_event


class EventBus:

    @staticmethod
    def publish(event):
        process_audit_event.delay(
            event_name=event.__class__.__name__,
            payload=asdict(event),
        )