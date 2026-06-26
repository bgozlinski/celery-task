from django.db import models
from django.conf import settings

from pathlib import Path


def available_templates():
    templates_dir = Path(settings.EMAIL_TEMPLATES_DIR)
    if not templates_dir.exists():
        return []
    return sorted(t.name for t in templates_dir.glob("*.html"))

class Mailbox(models.Model):
    """Sender mailbox"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    smtp_host = models.CharField(max_length=200)
    smtp_port = models.IntegerField()
    smtp_username = models.CharField(max_length=200)
    smtp_password = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "mailboxes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <<{self.email}>>"


class Message(models.Model):
    mailbox = models.ForeignKey(
        Mailbox,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    template_name = models.CharField(max_length=200) #e.g welkcome.html from templates/emails
    subject = models.CharField(max_length=200)
    receiver = models.EmailField()

    sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        state = "sent" if self.sent_at else "pending"
        return f"Message to {self.receiver} <<{state}>>"

