from emails.serializers import MailboxSerializer, MessageSerializer
from rest_framework import viewsets

from emails.models import Mailbox, Message
from emails.tasks import send_email_task

from django_filters.rest_framework import DjangoFilterBackend
from emails.filters import MessageFilter


class MailboxViewSet(viewsets.ModelViewSet):
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def perform_create(self, serializer):
        message = serializer.save()
        send_email_task.delay(message.id)

