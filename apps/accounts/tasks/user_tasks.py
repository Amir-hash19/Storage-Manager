from celery import shared_task
from apps.audit.services import AuditService




@shared_task
def process_audit_event(event_name, payload):

    AuditService.handle_event(
        event_name,
        payload
    )


