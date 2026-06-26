from rest_framework import serializers

from emails.models import Mailbox, Message, available_templates


class MailboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailbox
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["id", "created_at", "sent_at", "created_at"]

    def validate_mailbox(self, mailbox):
        if not mailbox.is_active:
            raise serializers.ValidationError("This mailbox is inactive")
        return mailbox

    def validate_template_name(self, value):
        templates = available_templates()
        if value not in templates:
            raise serializers.ValidationError("Template name is not available")
        return value
