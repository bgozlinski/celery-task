from django.contrib import admin

# Register your models here.
from emails.models import Mailbox, Message

@admin.register(Mailbox)
class MailboxAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "is_active" , "created_at")
    list_filter = ("is_active",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "receiver",
        "mailbox",
        "template_name" ,
        "subject",
        "sent_at",
        "created_at",
    )
    list_filter = ("sent_at", "created_at")
