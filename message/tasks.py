import logging
from celery import shared_task

_logger = logging.getLogger(__name__)


@shared_task
def dispatch_notifications():
    from event.models import Event
    from django.utils import timezone

    today = timezone.localdate()
    events = Event.objects.filter(
        event_date__date=today
    )
    for event in events:
        students = event.discipline.students.filter(
            notify_about_exams=True
        )
        for student in students:
            send_whatsapp_message_task(
                student.phone,
                f"Olá! Você tem um evento da disciplina de {event.discipline.name} hoje."
            )

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=30, retry_kwargs={'max_retries': 3})
def send_whatsapp_message_task(self, phone_number: str, message: str):
    from .services import WahaService

    return WahaService().send_message(
        phone_number=phone_number,
        message=message
    )
