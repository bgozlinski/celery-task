import logging
from celery import shared_task
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import timezone

from emails.models import Message


logger = logging.getLogger("emails")

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, message_id):
    try:
        message = Message.objects.select_related("mailbox").get(id=message_id)
        mailbox = message.mailbox

        if not mailbox.is_active:
            raise ValueError(f"Mailbox {mailbox.id} not active")

        html_body = render_to_string(
            f"emails/{message.template_name}",
            {"message": message},
        )

        connection = get_connection(
            host=mailbox.smtp_host,
            port=mailbox.smtp_port,
            username=mailbox.smtp_username,
            password=mailbox.smtp_password,
            use_tls=True,
        )

        email = EmailMultiAlternatives(
            subject=message.subject,
            body=html_body,
            from_email=mailbox.email,
            to=[message.receiver],
            connection=connection,
        )

        email.attach_alternative(html_body, "text/html")
        email.send()

        message.sent_at = timezone.now()
        message.save(update_fields=["sent_at"])
        logger.info("Email sent: message_id=%s", message_id)

    except Exception as e:
        logger.error("Failed to send email message_id=%s: %s", message_id, e)
        raise self.retry(exc=e)

