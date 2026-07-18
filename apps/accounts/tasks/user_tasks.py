from celery import shared_task
from apps.audit.services import AuditService
from apps.accounts.services.send_email_service import EmailService



@shared_task
def process_audit_event(event_name, payload):

    AuditService.handle_event(
        event_name,
        payload
    )


@shared_task
def process_email_event(event_name, payload):

    EmailService.handle_event(
        event_name,
        payload,
    )    