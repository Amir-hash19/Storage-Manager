from dataclasses import asdict
from apps.accounts.tasks.user_tasks import process_audit_event


class EventBus:

    @staticmethod
    def publish(event):
        payload = asdict(event)

        print(payload)
        print(type(payload["user_id"]))

        payload["user_id"] = str(payload["user_id"])

        process_audit_event.delay(
            event.__class__.__name__,
            payload,
        )