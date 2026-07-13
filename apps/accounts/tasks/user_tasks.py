from celery import shared_task
from apps.audit.services import AuditServices




@shared_task
def process_audit_event(event_name, payload):

    AuditServices.handle_event(
        event_name,
        payload
    )